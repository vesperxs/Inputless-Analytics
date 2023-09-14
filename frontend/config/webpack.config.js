const path = require("path");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const exclusions = /node_modules/;


module.exports = [
  {
      devtool: 'source-map',
      mode: 'development',

      entry: {
	  app: "./assets/app.js",
      },
      output: {
	  		path: path.resolve(__dirname, "/graph"),
	  		publicPath: "/static/",
	  		filename: "[name].js",
	  		chunkFilename: "[id]-[chunkhash].js",
      },
      devServer: {
	  host:'0.0.0.0',
	  port: 8081,
	  writeToDisk: true,
	  disableHostCheck: true,
	  inline:true,
	  hot:true
      },
      performance: {
	  hints: false
      },
      module: {
	  rules: [
	      {
		  test: /.*/,
		  include: path.resolve(__dirname, "assets/img"),
		  exclude: exclusions,
		  options: {
		      context: path.resolve(__dirname, "assets/"), 
		      name: "[path][name].[ext]",
		  },
		  loader: "file-loader"
	      },
	      {
		  test: /\.css$/,
		  exclude: exclusions,
		  use: [
		      MiniCssExtractPlugin.loader,
		      { loader: "css-loader" },
		  ],
	      },
	  ],
      },
      plugins: [
	  new CleanWebpackPlugin({ cleanStaleWebpackAssets: false }),
	  new MiniCssExtractPlugin(),
      ],
  }
];
