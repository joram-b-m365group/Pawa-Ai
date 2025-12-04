# 📁 Pawa AI Project Management - Complete Guide

## Overview

Pawa AI now includes a **Claude Code-style project management system** that lets you organize, track, and switch between multiple coding projects seamlessly!

---

## 🎯 Features

### 1. **Visual Project Manager**
- Beautiful grid layout with project cards
- Color-coded projects for easy identification
- Language and framework badges
- Quick search and filtering
- Multiple sort options

### 2. **Project Metadata**
- **Name & Description**: Clear project identification
- **Language & Framework**: Technology stack tracking
- **Tags**: Categorize projects (web, mobile, api, etc.)
- **Custom Colors**: 8 color themes to choose from
- **Timestamps**: Created date and last opened tracking

### 3. **Smart Features**
- **Favorites**: Star important projects for quick access
- **Recent Projects**: Auto-sorted by last opened time
- **Search**: Find projects by name, description, or tags
- **Inline Editing**: Update project details without leaving the manager

### 4. **Project Workflow**
- Create new projects with full metadata
- Browse local filesystem to select project path
- Switch between projects with one click
- Edit project details anytime
- Remove projects from list (doesn't delete files)

---

## 🚀 How to Use

### Opening the Project Manager

**Method 1: Keyboard Shortcut**
```
Ctrl+Shift+P (Windows/Linux)
Cmd+Shift+P (Mac)
```

**Method 2: UI Button**
Click the "Projects" button in the sidebar header

### Creating a New Project

1. Click **"New Project"** button (or press Ctrl+N in manager)
2. Fill in project details:
   - **Name**: Your project name (required)
   - **Path**: Absolute path to project folder (required)
   - **Description**: What the project does
   - **Language**: Primary programming language
   - **Framework**: Tech stack (React, Django, etc.)
   - **Color**: Choose a theme color
   - **Tags**: Comma-separated tags

3. Click **"Create Project"**

**Example:**
```
Name: E-Commerce Store
Path: C:\Users\Jorams\projects\ecommerce-store
Description: Full-stack e-commerce platform with payment processing
Language: TypeScript
Framework: Next.js 14
Color: Purple
Tags: web, frontend, fullstack, stripe
```

### Browsing for Project Path

1. In the create/edit dialog, click **"Browse"** next to path input
2. Navigate through your filesystem
3. Select the folder you want
4. Path will be automatically filled

### Switching Projects

**Method 1: Project Manager**
1. Open Project Manager (Ctrl+Shift+P)
2. Click on any project card
3. Project loads instantly!

**Method 2: Dropdown (if available)**
Use the project dropdown in the sidebar

### Managing Projects

**Edit a Project:**
1. Click the edit icon (pencil) on project card
2. Update any details
3. Click "Save Changes"

**Delete a Project:**
1. Click the trash icon on project card
2. Confirm deletion
3. Note: This only removes from list, doesn't delete files!

**Favorite a Project:**
- Click the star icon on project card
- Favorites appear at the top of the list

**Search Projects:**
- Type in the search box at the top
- Searches name, description, and tags
- Real-time filtering

**Sort Projects:**
- Use the sort dropdown:
  - **Recently Opened**: Most recent first (default)
  - **Name**: Alphabetical order
  - **Date Created**: Newest first

---

## 🎨 Project Colors

Choose from 8 theme colors:

| Color | Hex Code | Best For |
|-------|----------|----------|
| Purple | #8B5CF6 | General projects |
| Blue | #3B82F6 | Backend/APIs |
| Green | #10B981 | Production/Live |
| Yellow | #F59E0B | Experimental |
| Red | #EF4444 | Urgent/Priority |
| Pink | #EC4899 | Design/Frontend |
| Indigo | #6366F1 | Mobile apps |
| Teal | #14B8A6 | Data/Analytics |

---

## 📊 Project Statistics

Each project card shows:

- **Project name** and framework badge
- **Description** (2-line preview)
- **Tags** (first 3 visible, with +N indicator)
- **Last opened** time (relative, e.g., "2h ago")
- **Favorite status** (star icon)
- **Active project badge** (if currently open)

---

## 💡 Pro Tips

### 1. **Organize with Tags**
Use consistent tags across projects:
```
web, mobile, api, frontend, backend, fullstack,
personal, client, work, learning, prototype, production
```

### 2. **Color Coding System**
Create your own system:
- 🟣 Purple: Active projects
- 🔵 Blue: Backend services
- 🟢 Green: Completed/deployed
- 🟡 Yellow: In progress
- 🔴 Red: Needs attention
- 🩷 Pink: Client projects

### 3. **Naming Convention**
Use clear, consistent names:
```
✅ Good:
- E-Commerce Dashboard
- Task Manager API
- Portfolio Website v2

❌ Avoid:
- Project1
- test
- new-thing
```

### 4. **Quick Project Setup**
When starting a new project:
1. Create the folder structure first
2. Add to Pawa AI with full metadata
3. Use AI Agent to generate initial files
4. Files appear in VS Code instantly!

### 5. **Favorites for Daily Work**
Star the 3-5 projects you work on most:
- They'll always be at the top
- Faster to switch between
- Visual indicator of importance

---

## 🔄 Project Workflow Examples

### Example 1: Starting a New Web App

```
1. Create project folder: C:\projects\my-web-app
2. Open Pawa AI Project Manager
3. Click "New Project"
4. Fill details:
   - Name: My Web App
   - Path: C:\projects\my-web-app
   - Language: TypeScript
   - Framework: Next.js 14
   - Tags: web, frontend, nextjs
5. Create project
6. Open in VS Code (OPEN_IN_VSCODE.bat)
7. Ask AI Agent to create initial structure
8. Start coding!
```

### Example 2: Managing Multiple Client Projects

```
Client A - E-commerce (Purple, #client, #ecommerce)
Client B - Dashboard (Blue, #client, #dashboard)
Client C - API (Green, #client, #api)

- Star active client project
- Use colors to differentiate clients
- Tags help filter by client or type
- Sort by "Recently Opened" to see active work
```

### Example 3: Learning New Technologies

```
Learning React (Yellow, #learning, #react)
Learning Python (Yellow, #learning, #python)
Learning Go (Yellow, #learning, #golang)

- All marked with Yellow color
- Tagged with #learning
- Filter by tag to see all learning projects
- Track progress with descriptions
```

---

## 🔧 Technical Details

### Data Storage

Projects are stored in **localStorage** under key `pawa_projects`:

```typescript
interface Project {
  id: string                // Unique ID
  name: string              // Project name
  path: string              // Absolute file path
  description?: string      // Optional description
  language?: string         // Programming language
  framework?: string        // Framework/tech stack
  created: number           // Timestamp (ms)
  lastOpened: number        // Timestamp (ms)
  favorite: boolean         // Favorite flag
  color?: string            // Hex color code
  tags?: string[]           // Array of tag strings
}
```

### Component Architecture

```
ProjectManager.tsx
├── Project Card Grid
│   ├── Search & Sort
│   ├── Project Cards
│   │   ├── Metadata Display
│   │   ├── Action Buttons
│   │   └── Active Badge
│   └── Empty State
└── CreateProjectDialog
    ├── Form Inputs
    ├── Color Picker
    └── Path Browser
```

### Integration Points

1. **CodeStore**: Uses `currentProject` and `setCurrentProject`
2. **LocalStorage**: Persists project data
3. **ProjectBrowser**: Integrates for path selection
4. **UnifiedSidebar**: Shows in sidebar header

---

## 📝 Best Practices

### When to Create a Project

✅ **DO create projects for:**
- Any codebase you'll work on more than once
- Client projects (for easy switching)
- Learning exercises (to track progress)
- Open source contributions
- Personal portfolio pieces

❌ **DON'T create projects for:**
- One-time scripts
- Temporary test folders
- System directories
- Non-code folders

### Maintenance

**Weekly:**
- Review project list
- Remove completed/archived projects
- Update descriptions for active projects
- Re-organize favorites

**Monthly:**
- Clean up unused projects
- Review tagging system
- Archive old projects

---

## 🆚 Comparison with Other Tools

| Feature | Pawa AI | VS Code | Claude Code |
|---------|---------|---------|-------------|
| Visual Manager | ✅ | ❌ | ✅ |
| Metadata | ✅ Full | ⚠️ Basic | ✅ Full |
| Search | ✅ | ⚠️ Limited | ✅ |
| Favorites | ✅ | ❌ | ✅ |
| Color Coding | ✅ | ❌ | ❌ |
| Tags | ✅ | ❌ | ✅ |
| AI Integration | ✅ | ❌ | ✅ |

---

## 🐛 Troubleshooting

### Projects Not Saving

**Problem**: Projects disappear after page refresh

**Solution**:
1. Check browser localStorage is enabled
2. Clear browser cache and retry
3. Check browser console for errors

### Can't Find Project

**Problem**: Project doesn't appear in list

**Solution**:
1. Use search feature
2. Check if accidentally deleted
3. Sort by "Date Created" to see all projects
4. Create new project if needed

### Path Not Working

**Problem**: Can't browse to project folder

**Solution**:
1. Ensure path exists on filesystem
2. Use absolute paths (not relative)
3. Check folder permissions
4. Try manual path entry

---

## 🔮 Future Enhancements

Coming soon:
- ⏳ Project templates (React, Python, etc.)
- ⏳ Git integration (show branch, commits)
- ⏳ Project statistics (file count, lines of code)
- ⏳ Export/import project lists
- ⏳ Cloud sync across devices
- ⏳ Project groups/workspaces
- ⏳ Recent files per project
- ⏳ Project-specific AI context

---

## 📞 Quick Reference

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Open Manager | Ctrl+Shift+P |
| New Project | Ctrl+N (in manager) |
| Search | Type to filter |
| Close Manager | Esc |

### Project States

| State | Visual Indicator |
|-------|------------------|
| Active | "Active" badge + purple border |
| Favorite | Yellow star (filled) |
| Recent | High in "Recent" sort |

### Color Meanings (Suggested)

| Color | Use Case |
|-------|----------|
| 🟣 Purple | Active/current projects |
| 🔵 Blue | Backend/infrastructure |
| 🟢 Green | Completed/production |
| 🟡 Yellow | In progress/learning |
| 🔴 Red | Urgent/blocked |
| 🩷 Pink | Frontend/design |
| 🟦 Indigo | Mobile/native apps |
| 🔷 Teal | Data/analytics |

---

**Version**: Pawa AI v6.1
**Last Updated**: 2025-01-04
**Status**: Production Ready ✨

Happy coding with Pawa AI Projects! 🚀
