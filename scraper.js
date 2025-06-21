const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

puppeteer.use(StealthPlugin());

const PRIZEPICKS_URL = 'https://app.prizepicks.com/';
const API_ENDPOINT = 'https://api.prizepicks.com/projections';

async function fetchAllProps() {
    const browser = await puppeteer.launch({
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage'
        ]
    });

    const page = await browser.newPage();
    await page.goto(PRIZEPICKS_URL, { waitUntil: 'networkidle2' });

    const rawResponse = await page.evaluate(async (endpoint) => {
        const res = await fetch(endpoint);
        return res.json();
    }, API_ENDPOINT);

    await browser.close();

    const players = rawResponse.included.filter(i => i.type === 'new_player');
    const projections = rawResponse.data;

    const groupedProps = {};

    projections.forEach(proj => {
        const player = players.find(p => p.id === proj.relationships.new_player.data.id);
        const sport = proj.attributes.league;

        const entry = {
            name: player.attributes.name,
            stat_type: proj.attributes.stat_type,
            line_score: proj.attributes.line_score,
            game_time: proj.attributes.game_time,
            team: player.attributes.team,
            opponent: player.attributes.opponent
        };

        if (!groupedProps[sport]) groupedProps[sport] = [];
        groupedProps[sport].push(entry);
    });

    fs.writeFileSync('all_sports_props.json', JSON.stringify(groupedProps, null, 2));
    console.log('✅ Props saved to all_sports_props.json grouped by sport');
}

fetchAllProps();
