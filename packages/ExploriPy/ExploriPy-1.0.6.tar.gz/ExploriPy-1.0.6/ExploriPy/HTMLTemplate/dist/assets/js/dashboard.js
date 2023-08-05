require.config({
shim: {
'bootstrap': ['jquery'],
'sparkline': ['jquery'],
'tablesorter': ['jquery'],
'vector-map': ['jquery'],
'vector-map-de': ['vector-map', 'jquery'],
'vector-map-world': ['vector-map', 'jquery'],
'core': ['bootstrap', 'jquery'],
},
paths: {
'core': 'assets/js/core',
'jquery': 'assets/js/vendors/jquery-3.2.1.min',
'bootstrap': 'assets/js/vendors/bootstrap.bundle.min',
'sparkline': 'assets/js/vendors/jquery.sparkline.min',
'selectize': 'assets/js/vendors/selectize.min',
'tablesorter': 'assets/js/vendors/jquery.tablesorter.min',
'vector-map': 'assets/js/vendors/jquery-jvectormap-2.0.3.min',
'vector-map-de': 'assets/js/vendors/jquery-jvectormap-de-merc',
'vector-map-world': 'assets/js/vendors/jquery-jvectormap-world-mill',
'circle-progress': 'assets/js/vendors/circle-progress.min',
}
});
window.tabler = {
colors: {
'blue': '#467fcf',
'blue-darkest': '#0e1929',
'blue-darker': '#1c3353',
'blue-dark': '#3866a6',
'blue-light': '#7ea5dd',
'blue-lighter': '#c8d9f1',
'blue-lightest': '#edf2fa',
'azure': '#45aaf2',
'azure-darkest': '#0e2230',
'azure-darker': '#1c4461',
'azure-dark': '#3788c2',
'azure-light': '#7dc4f6',
'azure-lighter': '#c7e6fb',
'azure-lightest': '#ecf7fe',
'indigo': '#6574cd',
'indigo-darkest': '#141729',
'indigo-darker': '#282e52',
'indigo-dark': '#515da4',
'indigo-light': '#939edc',
'indigo-lighter': '#d1d5f0',
'indigo-lightest': '#f0f1fa',
'purple': '#a55eea',
'purple-darkest': '#21132f',
'purple-darker': '#42265e',
'purple-dark': '#844bbb',
'purple-light': '#c08ef0',
'purple-lighter': '#e4cff9',
'purple-lightest': '#f6effd',
'pink': '#f66d9b',
'pink-darkest': '#31161f',
'pink-darker': '#622c3e',
'pink-dark': '#c5577c',
'pink-light': '#f999b9',
'pink-lighter': '#fcd3e1',
'pink-lightest': '#fef0f5',
'red': '#e74c3c',
'red-darkest': '#2e0f0c',
'red-darker': '#5c1e18',
'red-dark': '#b93d30',
'red-light': '#ee8277',
'red-lighter': '#f8c9c5',
'red-lightest': '#fdedec',
'orange': '#fd9644',
'orange-darkest': '#331e0e',
'orange-darker': '#653c1b',
'orange-dark': '#ca7836',
'orange-light': '#feb67c',
'orange-lighter': '#fee0c7',
'orange-lightest': '#fff5ec',
'yellow': '#f1c40f',
'yellow-darkest': '#302703',
'yellow-darker': '#604e06',
'yellow-dark': '#c19d0c',
'yellow-light': '#f5d657',
'yellow-lighter': '#fbedb7',
'yellow-lightest': '#fef9e7',
'lime': '#7bd235',
'lime-darkest': '#192a0b',
'lime-darker': '#315415',
'lime-dark': '#62a82a',
'lime-light': '#a3e072',
'lime-lighter': '#d7f2c2',
'lime-lightest': '#f2fbeb',
'green': '#5eba00',
'green-darkest': '#132500',
'green-darker': '#264a00',
'green-dark': '#4b9500',
'green-light': '#8ecf4d',
'green-lighter': '#cfeab3',
'green-lightest': '#eff8e6',
'teal': '#2bcbba',
'teal-darkest': '#092925',
'teal-darker': '#11514a',
'teal-dark': '#22a295',
'teal-light': '#6bdbcf',
'teal-lighter': '#bfefea',
'teal-lightest': '#eafaf8',
'cyan': '#17a2b8',
'cyan-darkest': '#052025',
'cyan-darker': '#09414a',
'cyan-dark': '#128293',
'cyan-light': '#5dbecd',
'cyan-lighter': '#b9e3ea',
'cyan-lightest': '#e8f6f8',
'gray': '#868e96',
'gray-darkest': '#1b1c1e',
'gray-darker': '#36393c',
'gray-dark': '#6b7278',
'gray-light': '#aab0b6',
'gray-lighter': '#dbdde0',
'gray-lightest': '#f3f4f5',
'gray-dark': '#343a40',
'gray-dark-darkest': '#0a0c0d',
'gray-dark-darker': '#15171a',
'gray-dark-dark': '#2a2e33',
'gray-dark-light': '#717579',
'gray-dark-lighter': '#c2c4c6',
'gray-dark-lightest': '#ebebec'
}
};
require(['core']);