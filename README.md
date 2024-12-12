 <div class="register-container">
      <form
        action="/register"
        id="register"
        method="post"
        class="register-form"
      >
        <h1>Welcome</h1>
        <div id="common-fields">
          <div class="form-group">
            <label for="name">Full Name</label>
            <form action="/register" id="register" method="post">
              <input
                type="text"
                id="name"
                name="name"
                placeholder="Enter your full name"
                required
              />
            </form>
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              placeholder="Enter your email"
              required
            />
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input
              type="password"
              id="nif"
              name="NIF"
              placeholder="Enter your NIF"
              required
            />
          </div>
        </div>
        <div id="role-specific-fields"></div>
        <button type="submit" class="register-button">Register</button>
      </form>
    </div>
    <script></script>
