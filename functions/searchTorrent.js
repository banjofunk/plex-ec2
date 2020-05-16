const xtorrent = require('xtorrent');

module.exports.handler = async (event, context) => {
  const { query } = event;
  try {
    const torrentHref = await xtorrent.search({query}).then(({ torrents: [{ href }] }) => href);
    const torrentUrl = `https://1337x.to${torrentHref}`;
    const torrent = xtorrent.info(torrentUrl);
    return torrent;
  } catch (error) {
    return error
  }
};
