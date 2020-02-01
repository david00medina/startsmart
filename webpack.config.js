module.exports = {
	devServer: {
		historyApiFallback: true
	},
	module: {
		rules: [
			{
				test: /\.js$/,
				exclude: /node_modules/,
				use: {
					loader: "babel-loader"
				}
			},
			{
				test: /\.css?$/i,
				exclude: /\.module\.css$/i,
				use: ['style-loader', 'css-loader']
			},
			{
				// For CSS modules
				test: /\.module\.css$/i,
				use: [
				  	'style-loader',
				  	{
						loader: 'css-loader',
						options: {
					  		modules: true,
						},
			  		},
				],
		  	},
			{
				test: /\.(png|jpe?g|gif|svg|eot|ttf|woff|woff2)$/i,
				loader: 'url-loader',
				options: {
			  		limit: 8192,
				},
		  	},
		]
	}
}
