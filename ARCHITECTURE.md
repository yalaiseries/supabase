# AI Series Website - Architecture & Implementation Guide

## Table of Contents
1. [Overall Approach](#overall-approach)
2. [Technology Stack](#technology-stack)
3. [Setup & Deployment](#setup--deployment)
4. [Data Architecture](#data-architecture)
5. [Authentication Flow](#authentication-flow)
6. [Key Features](#key-features)
7. [Development Workflow](#development-workflow)

---

## Overall Approach

### Design Philosophy
The AI Series website is built as a **static frontend + serverless backend** architecture, combining:
- **Static HTML/CSS/JS** hosted on GitHub Pages for the public-facing site
- **Supabase** for authentication, database, and serverless edge functions
- **Members-only content** protected by authentication
- **Separation of concerns**: Public pages vs. protected resources

### Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                 FRONTEND (GitHub Pages)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  index   │  │ members  │  │ winners  │  │resources │   │
│  │  .html   │  │  .html   │  │  .html   │  │  .html   │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │              │             │          │
│       └─────────────┴──────────────┴─────────────┘          │
│                            │                                │
└────────────────────────────┼────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Supabase Auth  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌────────▼────────┐  ┌───────▼────────┐
│ Edge Functions │  │   PostgreSQL    │  │  Storage/Auth  │
│                │  │    Database     │  │                │
│ • winners      │  │                 │  │ • Sessions     │
│ • members-     │  │ • registrations │  │ • JWTs         │
│   resources    │  │ • winners_      │  │                │
│ • chat         │  │   payload       │  │                │
│ • register-    │  │                 │  │                │
│   sync         │  │                 │  │                │
│ • winners-     │  │                 │  │                │
│   admin        │  │                 │  │                │
└────────────────┘  └─────────────────┘  └────────────────┘
```

---

## Technology Stack

### Frontend
- **HTML5/CSS3/JavaScript** - Static, vanilla approach (no framework)
- **Supabase JS Client** - Authentication and API calls
- **GitHub Pages** - Static site hosting
- **Custom CSS** - Dark theme with modern design

### Backend (Supabase)
- **PostgreSQL Database** - Relational data storage
- **Edge Functions** (Deno runtime) - Serverless API endpoints
- **Supabase Auth** - JWT-based authentication
- **Row Level Security (RLS)** - Database access control (disabled for service_role reads)

### Development Tools
- **Git/GitHub** - Version control and collaboration
- **Python** - Data processing and uploads
- **PowerShell** - Windows automation scripts
- **VS Code** - Primary development environment

---

## Setup & Deployment

### Initial Setup

#### 1. Supabase Project Creation
```bash
# Install Supabase CLI
npm install -g supabase

# Initialize project
supabase init

# Link to remote project
supabase link --project-ref xcctqbamimafkkamuwly
```

#### 2. Database Schema
Located in `supabase/migrations/`:
- `20250103065556_add_registrations.sql` - User registrations table
- `20250103070234_add_winners_payload.sql` - Winners data storage

Key tables:
```sql
-- User registrations
CREATE TABLE registrations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text UNIQUE NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Winners data (members-only)
CREATE TABLE winners_payload (
  year int PRIMARY KEY,
  payload jsonb NOT NULL,
  updated_at timestamptz DEFAULT now(),
  challenge_topics jsonb
);
```

#### 3. Edge Functions Deployment
```bash
# Deploy all functions
supabase functions deploy winners
supabase functions deploy winners-admin
supabase functions deploy members-resources
supabase functions deploy chat
supabase functions deploy register-sync
```

#### 4. Secrets Configuration
```bash
# Set required secrets
supabase secrets set WINNERS_ADMIN_TOKEN=MySecureToken2025!
supabase secrets set OPENAI_API_KEY=sk-...
supabase secrets set SUPABASE_URL=https://xcctqbamimafkkamuwly.supabase.co
supabase secrets set SERVICE_ROLE_KEY=eyJh...
```

#### 5. GitHub Pages Deployment
- **Repository**: https://github.com/yalaiseries/supabase
- **Branch**: `main` (root directory)
- **URL**: https://yalaiseries.github.io/supabase/
- **Build settings**: None (static site)
- **Environment variables**: None required (client-side uses public keys)

---

## Data Architecture

### Database Tables

#### `registrations`
Stores registered members for access control.
```
┌──────────┬─────────┬──────────────┐
│ Column   │ Type    │ Purpose      │
├──────────┼─────────┼──────────────┤
│ id       │ uuid    │ Primary key  │
│ email    │ text    │ User email   │
│ created_at│ ts     │ Registration │
└──────────┴─────────┴──────────────┘
```

#### `winners_payload`
Stores winners data with challenge topics (members-only).
```
┌──────────────────┬─────────┬────────────────────────┐
│ Column           │ Type    │ Purpose                │
├──────────────────┼─────────┼────────────────────────┤
│ year             │ int     │ Competition year (PK)  │
│ payload          │ jsonb   │ Winners data structure │
│ challenge_topics │ jsonb   │ Year's challenge topics│
│ updated_at       │ ts      │ Last update timestamp  │
└──────────────────┴─────────┴────────────────────────┘
```

### Data Structures

#### Winners Payload Schema
```json
{
  "year": 2025,
  "categories": [
    {
      "category": "Top Winners",
      "useCases": [
        {
          "title": "Project Title",
          "team": "Team Name",
          "award": "1st Prize ($2500)",
          "people": {
            "lead": "Name",
            "coLeads": ["Name1", "Name2"],
            "teamMembers": ["Name3", "Name4"]
          },
          "showcase": {
            "problem": "Problem description",
            "proposedSolution": "Solution description",
            "approach": "Technical approach",
            "methods": "Methods used",
            "tools": "Tools and technologies",
            "impact": "Impact and outcomes"
          }
        }
      ]
    }
  ]
}
```

#### Challenge Topics Schema
```json
[
  {
    "code": "D",
    "title": "Design",
    "description": "Challenge description"
  }
]
```

### Edge Functions

#### `/winners` (GET)
**Purpose**: Fetch winners data for authenticated members  
**Authentication**: Required (JWT session)  
**Returns**: Winners payload + challenge topics

```typescript
// Request flow
User → winners.html → Supabase Auth (validate session) 
  → winners function → Check membership 
  → Load from DB → Return JSON
```

#### `/winners-admin` (POST)
**Purpose**: Upload/update winners data  
**Authentication**: Custom admin token (`x-admin-token`)  
**Accepts**: `{ year, payload, challenge_topics }`

```typescript
// Upload flow
Admin → curl/script → winners-admin function 
  → Validate token → Upsert to DB
```

#### `/members-resources` (GET)
**Purpose**: Fetch resources data for authenticated members  
**Authentication**: Required (JWT session)  
**Returns**: Resources JSON (future enhancement)

#### `/chat` (POST)
**Purpose**: AI chatbot for code questions  
**Authentication**: Required (JWT session)  
**Uses**: OpenAI API with RAG knowledge base

#### `/register-sync` (POST)
**Purpose**: Webhook for registration synchronization  
**Authentication**: Webhook secret  
**Triggered**: External registration system updates

---

## Authentication Flow

### Registration & Login

#### 1. User Registration
```
User fills Google Form → Admin adds to registrations table
  → Admin creates Supabase account with temporary password
  → User receives email with credentials → User logs in
```

#### 2. User Login
```
User enters email + password → Supabase Auth.signInWithPassword() 
  → Session created (JWT) → Redirected to members page
  → Access protected resources
```

**Password Reset Flow**:
```
User clicks "Email me a link" → Supabase Auth.resetPasswordForEmail()
  → Password reset email sent → User clicks link
  → Opens members page with recovery token → User sets new password
  → Supabase Auth.updateUser() → Password updated
```

#### 3. Session Management
```javascript
// On page load (all protected pages)
const session = await supabase.auth.getSession();
if (!session) {
  // Redirect to login or show error
  window.location.href = '/members.html';
}
```

### Protected Content Access

#### Members Page (`members.html`)
- Shows registration/login forms if not authenticated
- Displays welcome message if authenticated
- Gateway to protected resources

#### Winners Page (`winners.html`)
```javascript
// 1. Check authentication
const { data: { session } } = await supabase.auth.getSession();

// 2. Call protected endpoint
const response = await fetch(
  `${FUNCTIONS_URL}/winners`,
  {
    headers: {
      'Authorization': `Bearer ${session.access_token}`
    }
  }
);

// 3. Edge function validates membership
const membership = await requireRegisteredMember(req);
if (!membership.ok) return json({ error: 'Unauthorized' }, 401);

// 4. Return data
return json({ winners, challengeTopics });
```

#### Resources Page (`resources.html`)
- Similar authentication flow as winners page
- Currently shows static resources
- Prepared for future DB-backed resources

---

## Key Features

### 1. Challenge Topics Display
**Location**: Winners page  
**Purpose**: Show yearly challenge themes alongside winners

```html
<details class="challenge-section" open>
  <summary><strong>Challenge Topics</strong> · 2025</summary>
  <div class="challenge-topics-grid">
    <!-- Topic cards with code, title, description -->
  </div>
</details>
```

**Styling**: Blue theme with expandable sections

### 2. Winners Showcase
**Layout**: Two-column layout
- **Left**: Top Winners (1st, 2nd, 3rd prizes)
- **Right**: Innovation/Merit Awards

**Display Structure**:
```
┌─────────────────────────────────┐
│ Project Title                   │
│ ┌─────────────────────────────┐ │
│ │ 1st Prize ($2500)           │ │
│ └─────────────────────────────┘ │
│ Team 9                          │
│                                 │
│ ▼ Project Team                  │
│   Lead, Co-leads, Team members  │
│                                 │
│ ▼ Structured summary            │
│   Problem, Solution, Approach,  │
│   Methods, Tools, Impact        │
└─────────────────────────────────┘
```

### 3. Resources Hub
**Sections** (7 main categories):
1. Singapore AI Governance (priority placement)
2. Workflow Automation & Agents
3. Generative AI for Visualization
4. Massing and Design Tools
5. AECO and BIM Tools
6. Engineering and Analysis
7. Education and Standards

**Format**: Structured with explanations and video links

### 4. AI Chat Assistant
**Purpose**: Answer code-related questions  
**Implementation**: RAG-based chatbot using OpenAI  
**Knowledge Base**: Code examples, documentation, best practices

---

## Development Workflow

### Making Changes

#### 1. Update Frontend (HTML/CSS/JS)
```bash
# Edit files locally
code winners.html

# Test locally (open in browser)

# Commit and push
git add .
git commit -m "Description of changes"
git push

# GitHub Pages auto-deploys from main branch
```

#### 2. Update Edge Functions
```bash
# Edit function
code supabase/functions/winners/index.ts

# Test locally
supabase functions serve winners

# Deploy
supabase functions deploy winners
```

#### 3. Update Database Schema
```bash
# Create migration
supabase migration new description_of_change

# Edit migration file
code supabase/migrations/20250119_description_of_change.sql

# Apply migration
supabase db push
```

#### 4. Update Winners Data
```bash
# Edit JSON file
code data/winners-2025-corrected.json

# Upload to database
cd data
curl.exe -X POST https://xcctqbamimafkkamuwly.supabase.co/functions/v1/winners-admin \
  -H "Content-Type: application/json" \
  -H "x-admin-token: MySecureToken2025!" \
  -d "@temp-upload-2025.json"
```

### Configuration Files

#### `supabase/config.toml`
```toml
[functions.winners]
verify_jwt = false  # Custom auth in function

[functions.winners-admin]
verify_jwt = false  # Token-based auth
```

#### `supabase-config.js`
```javascript
// Client-side configuration
const SUPABASE_URL = 'https://xcctqbamimafkkamuwly.supabase.co';
const SUPABASE_ANON_KEY = 'eyJh...'; // Public key
```

---

## Security Considerations

### 1. Authentication
- ✅ JWT-based session management
- ✅ Email + password authentication
- ✅ Password reset via email link
- ✅ External registration (Google Forms)

### 2. Authorization
- ✅ Server-side membership validation
- ✅ Custom admin token for uploads
- ✅ Protected API endpoints

### 3. Data Protection
- ✅ Winners data behind authentication
- ✅ RLS disabled only for service_role
- ✅ Secrets stored in Supabase (not in code)

### 4. Public Keys
- ⚠️ `SUPABASE_ANON_KEY` is public (safe by design)
- ⚠️ Frontend code is visible (expected for static sites)
- ✅ Sensitive operations require server-side validation

---

## Troubleshooting

### Common Issues

#### 1. 401 Unauthorized on Winners Page
**Cause**: User not authenticated or not in registrations table  
**Fix**: 
- Ensure user is logged in
- Check `registrations` table for user's email
- Verify session token is valid

#### 2. Winners Data Not Showing
**Cause**: Data not in database or incorrect structure  
**Fix**:
- Check database: `SELECT * FROM winners_payload;`
- Verify JSON structure matches schema
- Re-upload using winners-admin endpoint

#### 3. Function Deployment Fails
**Cause**: Missing secrets or syntax errors  
**Fix**:
- Check `supabase secrets list`
- Review function logs: `supabase functions logs winners`
- Verify TypeScript syntax

#### 4. GitHub Pages Deploy Issues
**Cause**: Usually not applicable (static site)  
**Fix**: 
- Check GitHub Actions tab for deploy status
- Ensure all files are committed to Git
- Verify Pages is enabled (Settings → Pages)
- Confirm branch is set to `main` and folder to `/ (root)`

---

## Future Enhancements

### Planned Features
1. **Resources from Database**: Move resources.html content to DB
2. **Admin Dashboard**: Web UI for managing winners/resources
3. **Multi-year Filtering**: Better navigation for multiple years
4. **Search Functionality**: Full-text search across winners
5. **Analytics**: Track page views and popular content
6. **Comments/Discussion**: Member engagement features

### Scalability Considerations
- Current setup handles 1000s of users easily
- Supabase free tier limits: Monitor usage
- Consider CDN caching for static resources
- Database indexing for faster queries

---

## Contact & Support

**Project Repository**: https://github.com/yalaiseries/supabase  
**Live Site**: https://aihackathon.pro  
**GitHub Pages (alternate)**: https://yalaiseries.github.io/supabase/  
**Supabase Project**: xcctqbamimafkkamuwly.supabase.co  
**Deployment**: GitHub Pages with custom domain (auto-deploy from main branch)

For questions or issues, refer to:
- This documentation
- Supabase docs: https://supabase.com/docs
- Edge Functions guide: https://supabase.com/docs/guides/functions
