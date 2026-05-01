# CLAUDE.md

This file provides guidance to AI Agent when working with the frontend codebase.

## Project Overview

React 19 SPA template with client-side routing, an accessible component library, and utility-first styling. Designed as a starter for multi-page applications with nested layouts.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| React 19 | UI framework |
| React Router 7 | Client-side routing (declarative mode) |
| Vite | Build tool + dev server |
| Tailwind CSS v4 | Utility-first styling |
| shadcn/ui | Pre-built accessible components (radix-lyra preset) |
| Radix UI | Headless UI primitives (via shadcn) |
| Lucide React | Icon library |
| clsx + tailwind-merge | Class name merging |
| class-variance-authority | Component variant definitions |
| Geist + JetBrains Mono | Variable fonts |
| ESLint | Linting (flat config) |

---

## Commands

```bash
# Development
npm run dev

# Build
npm run build

# Preview production build
npm run preview

# Lint
npm run lint
```

---

## Architecture

```
frontend/
├── src/
│   ├── main.jsx              # React entry, mounts to #root
│   ├── App.jsx               # Root router + all route definitions
│   ├── index.css             # Global styles + Tailwind directives
│   ├── layouts/              # Shell components (render <Outlet />)
│   │   └── RootLayout.jsx    # App-wide header + Outlet
│   ├── pages/                # Route-level components
│   │   ├── Home.jsx
│   │   ├── About.jsx
│   │   ├── NotFound.jsx
│   │   └── dashboard/
│   │       ├── Dashboard.jsx       # Nested layout wrapper
│   │       ├── DashboardHome.jsx   # Index route
│   │       └── Settings.jsx
│   ├── components/
│   │   ├── ui/               # shadcn/ui generated — do not edit manually
│   │   └── PageHeader.jsx    # Custom component example
│   ├── lib/
│   │   └── utils.js          # cn() helper
│   └── assets/               # Images, SVGs
├── public/                   # Static files served as-is
├── components.json           # shadcn config (theme, aliases, icons)
├── vite.config.js            # Vite + Tailwind plugin + @ alias
└── jsconfig.json             # @ → ./src path alias
```

---

## Code Patterns

### Naming Conventions
- Components: PascalCase, one per file (`PageHeader.jsx`)
- Pages: PascalCase, mirror route structure (`DashboardHome.jsx`)
- Utilities: camelCase (`utils.js`)
- Hooks: `use` prefix (`useLocalStorage.js`)

### File Organization
- Pages in `src/pages/`, grouped by feature/route in subdirectories
- Layouts in `src/layouts/` — shell UI only, no data fetching
- Custom components in `src/components/`, shadcn-generated in `src/components/ui/`
- Shared logic in `src/lib/`

### Imports
- Always use `@/` alias (`@/components/ui/button`, `@/layouts/RootLayout`)
- Never traverse up more than one level with relative paths

### Styling
- Tailwind classes only — no inline styles, no CSS modules
- Use `cn()` from `@/lib/utils` for conditional/merged class names
- Component variants via `class-variance-authority`

### Component pattern
```jsx
import { cn } from "@/lib/utils"

export default function MyComponent({ className, children, ...props }) {
  return (
    <div className={cn("base-classes", className)} {...props}>
      {children}
    </div>
  )
}
```

### Routing
- All routes in `App.jsx` using React Router declarative mode
- Layouts: pathless `<Route element={<Layout />}>` wraps child routes
- Navigation: `<Link>` or `<NavLink>` — never raw `<a href>`
- Nested layouts render `<Outlet />` for child route injection

```jsx
<Route element={<RootLayout />}>
  <Route path="/" element={<Home />} />
  <Route path="dashboard" element={<Dashboard />}>
    <Route index element={<DashboardHome />} />
    <Route path="settings" element={<Settings />} />
  </Route>
  <Route path="*" element={<NotFound />} />
</Route>
```

### Error Handling
- 404: catch-all `<Route path="*" element={<NotFound />} />`
- No global error boundary yet — add `<ErrorBoundary>` at layout level if needed

---

## Testing

No test suite configured. Validate in browser via `npm run dev`.

---

## Validation

```bash
npm run lint && npm run build
```

---

## Key Files

| File | Purpose |
|------|---------|
| `src/App.jsx` | All route definitions |
| `src/layouts/RootLayout.jsx` | App-wide layout shell |
| `src/index.css` | Global styles, CSS variables, Tailwind import |
| `src/lib/utils.js` | `cn()` class merge helper |
| `components.json` | shadcn theme and alias config |
| `vite.config.js` | Build config + `@` path alias |

---

## On-Demand Context

| Topic | Skill |
|-------|-------|
| React Router routes, Outlet, NavLink, URL params | `/react-router-declarative-mode` |
| shadcn components, theming, CLI usage | `/shadcn` |

---

## Notes

- JavaScript only — no TypeScript (`jsconfig.json` provides editor support + `@` alias)
- Tailwind v4: use `@import "tailwindcss"` in CSS, not legacy `@tailwind` directives
- shadcn theme: `radix-lyra` style, `taupe` base color, CSS variables enabled
- Icons: always import from `lucide-react` (configured in `components.json`)
- `src/components/ui/`: shadcn-generated files — update via CLI, not by hand
