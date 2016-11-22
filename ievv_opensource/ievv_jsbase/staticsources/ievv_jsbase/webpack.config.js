const is_production = process.env.IEVV_BUILDSTATIC_MODE == 'production';

module.exports = {
  entry: './scripts/javascript/ievv_jsbase/ievv_jsbase_core.js',
  output: {
    filename: 'bundle.js',
    path: './dist'
  },
  module: {
    loaders: [
      {
        test: /.jsx?$/,
        loader: 'babel-loader'
        // exclude: /node_modules/
      }
    ]
  }
};
