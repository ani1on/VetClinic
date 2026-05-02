const { defineConfig } = require('@vue/cli-service')

const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',   // todo добавить порт апишника
        changeOrigin: true,
      },
    },
  },
});
module.exports = defineConfig({
  transpileDependencies: true
})
