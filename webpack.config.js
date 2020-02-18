module.exports = {
	devServer: {
		historyApiFallback: true
	},
	resolve: {
		modules:  [
			'node_modules',
			'apps/frontend/src',
			'apps/frontend/static',
			'apps/frontend/templates',
			'apps/frontend/lib'
		]
	},
	module: {
		rules: [
			{
				test: /\.(js|jsx)$/,
				exclude: /node_modules/,
				use: {
					loader: "babel-loader",
				},
			},
			{
				test: /\.s[ac]ss$/i,
				use: [
				  // Creates `style` nodes from JS strings
				  'style-loader',
				  // Translates CSS into CommonJS
				  'css-loader',
				  // Compiles Sass to CSS
				  'sass-loader',
				],
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
