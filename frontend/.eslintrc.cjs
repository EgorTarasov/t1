/** @type {import('eslint').Linter.Config} */
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    "eslint:recommended",
    // 'plugin:@typescript-eslint/recommended-type-checked', tooooo strict for hackathon
    "plugin:@typescript-eslint/stylistic-type-checked",
    "plugin:react-hooks/recommended",
    "plugin:react/recommended",
    "plugin:react/jsx-runtime",
    "plugin:prettier/recommended"
  ],
  ignorePatterns: ["dist", ".eslintrc.cjs"],
  parser: "@typescript-eslint/parser",
  plugins: ["react-refresh"],
  rules: {
    "react-refresh/only-export-components": [
      "warn",
      { allowConstantExport: true }
    ],
    "@typescript-eslint/no-namespace": "off",
    "@typescript-eslint/no-unused-vars": "off",
    "react/prop-types": "off",
    "no-unused-vars": "off",
    "@typescript-eslint/prefer-nullish-coalescing": "warn",
    "react/display-name": "off"
  },
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
    project: ["./tsconfig.json", "./tsconfig.node.json"],
    tsconfigRootDir: __dirname
  }
};
