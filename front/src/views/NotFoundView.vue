<template>
  <section class="page not-found">
    <div class="hero-card" style="text-align: center;">
      <div class="not-found-content">
        <div class="not-found-icon">🔍</div>
        <h1 class="hero-title">404</h1>
        <p class="hero-subtitle">Страница не найдена</p>
        <p class="muted">Извините, запрашиваемая страница не существует или была перемещена.</p>
        <div class="hero-actions" style="justify-content: center;">
          <router-link to="/" class="button">На главную</router-link>
          <router-link to="/catalog" class="button-secondary">Перейти в каталог</router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "NotFoundView"
};
</script>

<style scoped>
.not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}
.not-found-content {
  max-width: 500px;
  margin: 0 auto;
}
.not-found-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}
</style>