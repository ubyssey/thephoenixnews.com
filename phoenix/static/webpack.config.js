var webpack = require('webpack');
var version = require('./package.json').version;
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var CopyWebpackPlugin = require('copy-webpack-plugin');
var globImporter = require('node-sass-glob-importer');

module.exports = {
  entry: {
    index: './src/js/index',
    pdf: './src/js/pdf',
    'pdf.worker': 'pdfjs-dist/build/pdf.worker.entry',
  },
  output: {
    path: __dirname + '/dist',
    filename: '[name]-' + version + '.js'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: { loader: 'babel-loader' },
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        enforce: 'pre',
        use: {
          loader: 'eslint-loader',
          options: {
            emitWarning: true,
          }
        }
      },
      {
        test: /\.scss$/,
        exclude: /node_modules/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: [
            {
              loader: 'css-loader'
            },
            {
              loader: 'sass-loader',
              options: {
                importer: globImporter()
              }
            }
          ]
        }),
      },
      {
        test: /\.(png|jpg|svg|gif|woff|woff2|eot|ttf)$/,
        use: { loader: 'url-loader?limit=100000' }
      }
    ]
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('production')
      }
    }),
    new CopyWebpackPlugin([{
      from: './src/images/public/',
      to:''
    }]),
    new webpack.optimize.UglifyJsPlugin(),
    new ExtractTextPlugin('main-' + version + '.css')
  ]
};
