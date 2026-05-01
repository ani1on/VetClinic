<template>
  <section class="page">
    <div class="section-heading">
      <div>
        <h1 class="section-title">Profile</h1>
        <p class="section-copy">
          Personal cabinet with owner data, pet cards, prescriptions and the next appointments.
        </p>
      </div>
    </div>

    <section class="split-grid">
      <article class="panel">
        <h2 class="section-title">Owner card</h2>
        <div class="form-grid two">
          <label class="field">
            <span>Full name</span>
            <input type="text" value="Anna Petrova" />
          </label>
          <label class="field">
            <span>Phone</span>
            <input type="text" value="+375 29 456-88-00" />
          </label>
          <label class="field">
            <span>Email</span>
            <input type="email" value="anna@fastpig.by" />
          </label>
          <label class="field">
            <span>City</span>
            <input type="text" value="Minsk" />
          </label>
        </div>
        <div class="hero-actions">
          <button class="button" type="button">Save changes</button>
        </div>
      </article>

      <article class="panel">
        <h2 class="section-title">Pet cards</h2>
        <div class="list-column">
          <article class="feed-card">
            <div class="meta-row">
              <strong>Peppa</strong>
              <span class="chip">Mini pig</span>
            </div>
            <p class="muted">2 years old, female, allergies noted, vaccine active until Nov 2026.</p>
          </article>
          <article class="feed-card">
            <div class="meta-row">
              <strong>Boris</strong>
              <span class="chip">Dog</span>
            </div>
            <p class="muted">7 years old, joint care program, next analysis in two weeks.</p>
          </article>
        </div>
      </article>
    </section>

    <section class="panel">
      <h2 class="section-title">History and recommendations</h2>
      <div class="tile-grid">
        <article class="tile soft">
          <h3 class="card-title">Medical history</h3>
          <p class="muted">Visits, diagnoses, lab results and attached files from the backend.</p>
        </article>
        <article class="tile soft success">
          <h3 class="card-title">Prescriptions</h3>
          <p class="muted">Current medication plans and dosage reminders for each pet.</p>
        </article>
        <article class="tile soft warn">
          <h3 class="card-title">Recommendations</h3>
          <p class="muted">Doctor tips, repeat purchases and preventive procedures.</p>
        </article>
      </div>
    </section>
  </section>
</template>

<script>
export default {
  name: "ProfileView",
};
</script>
