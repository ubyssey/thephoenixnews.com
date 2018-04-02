module.exports = {
  "env": {
    "browser": true,
    "commonjs": true,
    "es6": true,
    "node": true,
  },
  "extends": ["eslint:recommended",],
  "parserOptions": {
    "sourceType": "module",
    "ecmaFeatures": {
      "jsx": true
    }
  },
  "rules": {
    "indent": ["error", 2],
    "linebreak-style": 0,
    "quotes": ["error", "single"],
    "no-unused-vars": ["warn", {"args": "after-used"}],
    "no-console": ["warn"],
  }
};
