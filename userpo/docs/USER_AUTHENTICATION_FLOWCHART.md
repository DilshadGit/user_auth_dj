# User Authentication Flow — Multi-Section Process Design

```mermaid
flowchart TB
    subgraph P1["01. Access & Onboarding"]
        A[Visitor opens application]
        B{Has account?}
        C[Open sign-up form]
        D[Enter email, password, and profile details]
        E[Validate form data]
        F{Valid?}
        G[Show field errors]
        H[Create CustomUser record]
        I[Assign role and profile metadata]
    end

    subgraph P2["02. Login & Security Checks"]
        J[Go to login page]
        K[Enter email and password]
        L{Credentials valid?}
        M{Too many failed attempts?}
        N[Activate django-axes lockout]
        O[Show security message]
        P[Create authenticated session]
        Q{Account active and not deleted?}
        R[Reject access]
    end

    subgraph P3["03. Authorization & User Experience"]
        S{Assigned role?}
        T[Member access]
        U[Staff access]
        V[Admin access]
        W[Profile and personal settings]
        X[Dashboard and user management]
        Y[Search users and review audit data]
    end

    subgraph P4["04. Recovery, Logout & Continuity"]
        Z[Password reset request]
        AA[Generate secure reset token]
        AB[Send email reset link]
        AC[Confirm new password]
        AD[Update password securely]
        AE[Logout]
        AF[Clear session and tracking data]
        AG[Secure user state restored]
    end

    A --> B
    B -- No --> C --> D --> E --> F
    F -- No --> G --> C
    F -- Yes --> H --> I --> J
    B -- Yes --> J

    J --> K --> L
    L -- No --> M
    M -- Yes --> N --> O --> J
    M -- No --> O --> J
    L -- Yes --> P --> Q
    Q -- No --> R
    Q -- Yes --> S

    S -- Member --> T --> W
    S -- Staff --> U --> X
    S -- Admin --> V --> X
    X --> Y

    W --> Z
    X --> Z
    V --> Z
    Z --> AA --> AB --> AC --> AD --> J

    W --> AE --> AF --> AG
    X --> AE --> AF --> AG
    Y --> AE --> AF --> AG
```

## Flow explanation

This flowchart is structured in four main sections, inspired by a real-world system design layout:

1. Access & Onboarding
2. Login & Security Checks
3. Authorization & User Experience
4. Recovery, Logout & Continuity

The process moves from visitor to registered user, then to authenticated access, then to role-based authorization, and finally to secure recovery and logout states.

This keeps the design visual, process-oriented, and closer to a professional system architecture diagram rather than plain text-only explanation.
