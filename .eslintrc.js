/* eslint-env node */

module.exports = {
  "root": true,
  "extends": ["eslint:recommended"],
  "env": {
    "node": true,
    "es2021": true,
  },
  "overrides": [
    {
      "files": ["**/*.ts", "**/*.tsx"],
      "parser": "@typescript-eslint/parser",
      "plugins": [
        "@typescript-eslint"
      ],
      "extends": [
        "eslint:recommended",
        "plugin:@typescript-eslint/eslint-recommended",
        "plugin:@typescript-eslint/recommended"
      ]
    }
  ],
  "ignorePatterns": ["dist/*", "node_modules/*"],
  "rules": {
    "quotes": ["error", "double"]
  }
}
