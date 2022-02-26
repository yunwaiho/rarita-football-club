const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const Fuse = require('fuse.js');
const removeAccents = require('remove-accents');

/*
    this is a script that scrapes soccer player market value from a specific 
    tournament, given the fbref data of the players

    to use this script, change the variables below,
    get node.js install all the modules above, and run the command
    > node scrape.js

    note that there may be values missing that needs to be manually fixed
    (search for N/A in the data)
*/

// seach in uefa champion league <year/year+1>
// ie: year: '2020' means 20/21
const league = {
    url: '/uefa-champions-league/teilnehmer/pokalwettbewerb/CL/', 
    year: '2019'
}

// fbref data of players that we wish to find market value of
// data should only contain the fields: <Player>, <Squad>, <Born>
// in comma delimited format
const fbrefData = 'fbref_player.txt';

// ----------------------------------------------------------------------------

const uefa = {};
const transfermarkt = 'https://www.transfermarkt.com'

// scrape data of each team
async function scrapeTeams(league) {
    try {
        const url = transfermarkt + league.url + 'saison_id/' + league.year;
        const { data } = await axios.get(url);
        const $ = cheerio.load(data);

        // contains all teams participated in the league
        const teams = $('[class="links no-border-links hauptlink"]');

        // scrape team data into object
        teams.each((idx, el) => {
            const teamName = $(el).children().text();
            const teamUrl = $(el).children().attr('href');
            uefa[teamName] = {url: teamUrl}
        })
    } catch (err) {
        console.error(err);
    }
}

// scrape squad information of a team at a particular year
async function scrapeSquad(year, teamUrl) {
    try {
        const url = transfermarkt + teamUrl + '?saison_id=' + league.year;
        const { data } = await axios.get(url);
        const $ = cheerio.load(data);

        // selects all players within the team
        const players = $('.odd, .even', $('tbody').get(1));
        
        console.log('scraping ' + teamUrl);
        
        let playerList = [];
        players.each((idx, el) => {
            const player = {}
            const playerProfile = $('.show-for-small', el).children();
            player.name = playerProfile.attr('title');
            player.url = playerProfile.attr('href');

            const playerDOB = $('[class=zentriert]', el).get(0);
            player.year = $(playerDOB).text().match(/\d{4}/)[0];
            
            const playerMV = $('.rechts.hauptlink', el).text();
            player.mv = convertMV(playerMV.trim());
            playerList.push(player);
        })

        console.log('number: ' + playerList.length)
        
        return playerList;
    } catch (err) {
        console.error(err);
    }
}

// converts transfermarkt market value into numbers
function convertMV(mv) {
    if (mv == '') {
        return 'N/A';
    }

    // remove currency symbol
    mv = mv.slice(1);
    // find index where unit begins
    const index = mv.search(/[a-z]/i);
    
    const number = mv.slice(0, index);
    const unit = mv.slice(index);

    const m = 1000000;
    const th = 1000;
    
    let value;

    if (unit == 'm') {
        value = parseFloat(number) * m;
    } else {
        value = parseFloat(number) * th;
    }
    
    return value.toString();
}

// cleans fbref data
function clean_fbref() {
    const fbref = fs.readFileSync(fbrefData).toString().replace(/\r\n/g, "\n").split('\n');
    
    // clean header
    let head = fbref[0].split(',');
    head.splice(1, 0, 'fbref id');
    fs.writeFileSync('cleaned_fbref.txt', head.join(','));

    // clean actual data
    for (let i = 1; i < fbref.length; i++) {
        let line = fbref[i].split(',');

        line.splice(1, 0, line[0].split('\\')[1]);
        line[0] = line[0].split('\\')[0];

        line[2] = line[2].split(' ').splice(1).join(' ');
        fs.appendFileSync('cleaned_fbref.txt', '\n'+line);
    }
}

function match() {
    const fbref = fs.readFileSync('cleaned_fbref.txt').toString().split('\n');
    
    // make header
    const header = fbref[0].split(',');
    header.splice(2, 0, 'transm id', 'mv');
    header.splice(-2);
    fs.writeFileSync('player_mv.csv', header.join(','));

    // search for team
    const teamSearch = new Fuse(Object.keys(uefa));

    for (let i = 1; i < fbref.length; i++) {
        const line = fbref[i].split(',');
        line[0] = removeAccents(line[0]);
        const team = teamSearch.search(line[2])[0].item;

        // search for player
        const options = {
            keys: ["name"]
        }
        const playerSearch = new Fuse(uefa[team].players, options);
        const player = playerSearch.search(line[0])[0];

        // found player!
        if (player != undefined) {
            // match this with their birth year
            if (player.item.year == line[3]) {
                // add player to csv
                line.splice(-2);
                player.item.url.split('/');
                line.splice(2, 0, player.item.url.split('/').at(-1), player.item.mv);
                
                fs.appendFileSync('player_mv.csv', '\n'+line.join(','));
                continue;
            }
        }

        // when player is not found
        const teamUrl = transfermarkt + uefa[team].url + '?saison_id=' + league.year;
        line.splice(2, 0, teamUrl, line[3], 'N/A');
        line.splice(-2);
        fs.appendFileSync('player_mv.csv', '\n'+line.join(','));
    }
}

async function run() {
    await scrapeTeams(league);
    
    for (const team in uefa) {
        const players = await scrapeSquad(league.year, uefa[team].url);
        uefa[team].players = players;
    }
    
    clean_fbref();
    match();
}

run();
