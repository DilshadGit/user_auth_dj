# User Authentication Flow

<div class="stage-nav">
  <a href="#stage-1" class="active">Stage 1</a>
  <a href="#stage-2">Stage 2</a>
  <a href="#stage-3">Stage 3</a>
  <a href="#stage-4">Stage 4</a>
</div>

<div class="stage-page" id="stage-1">
  <div class="stage-header">
    <span class="stage-number">01</span>
    <div>
      <p class="stage-label">Access &amp; Onboarding</p>
      <h2>New users begin their journey</h2>
    </div>
  </div>

  <p class="stage-summary">A visitor enters the system, signs up, validates their information, and completes account creation before being allowed into the application.</p>

  <pre class="mermaid">
  flowchart LR
      s1A[Visitor] --> s1B[Sign up]
      s1B --> s1C[Validate data]
      s1C --> s1D[Create account]
  </pre>
</div>

<div class="stage-page" id="stage-2">
  <div class="stage-header">
    <span class="stage-number">02</span>
    <div>
      <p class="stage-label">Login &amp; Security</p>
      <h2>Authentication is verified and protected</h2>
    </div>
  </div>

  <p class="stage-summary">The user submits credentials, the platform checks validity, and the system blocks repeated failures with lockout safeguards before creating a secure session.</p>

  <pre class="mermaid">
  flowchart LR
      s2E[Login] --> s2F{Valid login?}
      s2F -->|No| s2G[Lockout / retry check]
      s2G --> s2E
      s2F -->|Yes| s2H[Create session]
  </pre>
</div>

<div class="stage-page" id="stage-3">
  <div class="stage-header">
    <span class="stage-number">03</span>
    <div>
      <p class="stage-label">Authorization &amp; Role Access</p>
      <h2>Permissions define the user experience</h2>
    </div>
  </div>

  <p class="stage-summary">Once authenticated, user roles decide what area they can enter: member profile, staff dashboard, or admin dashboard.</p>

  <pre class="mermaid">
  flowchart LR
      s3I{Role}
      s3I -->|Member| s3J[Member profile]
      s3I -->|Staff| s3K[Staff dashboard]
      s3I -->|Admin| s3L[Admin dashboard]
  </pre>
</div>

<div class="stage-page" id="stage-4">
  <div class="stage-header">
    <span class="stage-number">04</span>
    <div>
      <p class="stage-label">Recovery &amp; Continuity</p>
      <h2>Secure account recovery and exit</h2>
    </div>
  </div>

  <p class="stage-summary">Users can recover access when needed and then safely end the session. This keeps the platform secure and makes the process resilient for real-world use.</p>

  <pre class="mermaid">
  flowchart LR
      s4J[Member profile] --> s4M[Reset password]
      s4K[Staff dashboard] --> s4M
      s4L[Admin dashboard] --> s4M
      s4J --> s4N[Logout]
      s4K --> s4N
      s4L --> s4N
  </pre>
</div>

<div class="stage-summary-box">
  <strong>Overall flow:</strong> visitors sign up, authenticate securely, receive role-based access, and then either recover or exit the system safely.
</div>
