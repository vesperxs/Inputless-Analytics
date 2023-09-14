const path = require("path");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
var WebpackObfuscator = require('webpack-obfuscator');

const exclusions = /node_modules/;

module.exports = [
    {
	mode:'production',
	entry: {
		app: "./assets/app.js",
		},


	output: {
	    path: path.resolve(__dirname, "./graph"),
	    publicPath: "/static/",
	    filename: "[name].js",
	    chunkFilename: "[id]-[chunkhash].js",
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
		{
			test: /\.js$/,
			exclude:exclusions, 
			enforce: 'post',
			use: { 
				loader: WebpackObfuscator.loader, 
				options: {
					rotateStringArray: true
				}
			},
		},
	    ],
	},
	plugins: [
	    new CleanWebpackPlugin({ cleanStaleWebpackAssets: false }),
	    new MiniCssExtractPlugin(),
		new WebpackObfuscator ({
        	rotateStringArray: true
    	}, ['excluded_bundle_name.js'])
	],
	
    },
];
