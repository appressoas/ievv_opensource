let path = require('path');

const appconfig = require("./ievv_buildstatic.appconfig.json");
console.log(appconfig);

let webpackConfig = {
    entry: path.resolve(__dirname, 'scripts/javascript/ievv_jsbase/ievv_jsbase_core.js'),
    output: {
        filename: 'ievv_jsbase_core.js',
        path: path.resolve(appconfig.destinationfolder, 'scripts')
    },
    module: {
        loaders: [
            {
                test: /.jsx?$/,
                loader: 'babel-loader',
                // exclude: /node_modules/
                include: [
                    path.resolve(__dirname, "scripts/javascript/ievv_jsbase"),
                ]
            }
        ]
    }
};

if(appconfig.is_in_production_mode) {
    webpackConfig.devtool = 'source-map';
} else {
    webpackConfig.devtool = 'cheap-module-eval-source-map';
    webpackConfig.output.pathinfo = true;
}


module.exports = webpackConfig;
