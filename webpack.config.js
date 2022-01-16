const path = require('path');

module.exports = {
  entry: './frontend/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist'),
  },
};
