const path = require("path");

const HtmlWebpackPlugin = require("html-webpack-plugin")


module.exports = {
  entry: "./frontend/index.tsx",
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
    ],
  },
  output: {
    filename: "main.js",
    path: path.resolve(__dirname, "dist"),
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "./frontend/index.html",
      favicon: "./assets/favicon/favicon.ico"
    })
  ],
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
  },
};
