# SwasthAI Admin Panel

## Overview
The SwasthAI Admin Panel provides comprehensive management capabilities for monitoring users and their interactions with the AI healthcare assistant.

## Features

### 📊 Dashboard
- **Real-time Statistics**:
  - Total registered users
  - Total messages exchanged
  - New users in the last 7 days
  - Average messages per user
- **Recent Users Table**: Quick view of the 5 most recent registrations

### 👥 User Management
- **View All Users**: Complete list with filtering and sorting
- **User Details**:
  - ID, Username, Full Name
  - Role (Admin/User)
  - Total message count
  - Registration date
- **User Actions**:
  - View complete chat history for any user
  - Delete user accounts (with confirmation)
  - Cannot delete your own admin account

### 💬 Chat History Viewer
- View all conversations for any user
- Color-coded messages:
  - Blue: User messages
  - Green: AI Assistant responses
- Timestamps for each message
- Complete conversation context

## Setup Instructions

### 1. Database Migration
The admin feature requires an `is_admin` column in the User table. This will be automatically created when you restart the application.

If you have existing users, you can manually update the database:

```sql
-- SQLite
ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0 NOT NULL;
```

### 2. Create Your First Admin User

Run the admin creation script:

```bash
# Activate virtual environment
.\SwasthAI\Scripts\activate  # Windows
source SwasthAI/bin/activate  # Linux/Mac

# Run the script
python create_admin.py
```

Follow the prompts to create your admin account:
- Enter admin username
- Enter full name
- Enter secure password

### 3. Access Admin Panel

1. Start the application:
```bash
python main.py
```

2. Navigate to: `http://localhost:8000/admin`

3. You'll be redirected to login if not authenticated

4. Login with your admin credentials

5. Access the admin dashboard

## Admin Panel Routes

### Frontend Routes
- `/admin` - Admin Dashboard (requires admin authentication)

### API Routes (Admin Only)
All routes require admin authentication via JWT token:

- `GET /api/admin/users` - Get all users with statistics
- `GET /api/admin/users/{user_id}/messages` - Get user's chat history
- `GET /api/admin/stats` - Get platform statistics
- `DELETE /api/admin/users/{user_id}` - Delete a user

## Security Features

✅ **Role-Based Access Control**
- Only users with `is_admin=True` can access admin features
- JWT token validation on every request
- Automatic redirect to login for unauthenticated access

✅ **Protected Actions**
- Cannot delete your own admin account
- Confirmation dialog for user deletion
- Read-only view of user chat histories

✅ **No Search Engine Indexing**
- `robots.txt` configured to block `/admin` route
- `noindex, nofollow` meta tags on admin pages

## UI/UX Features

### Design Consistency
- Follows the same theme as main SwasthAI application
- Color scheme:
  - Primary: `#1e40af` (Blue)
  - Success: `#10b981` (Green)
  - Warning: `#f59e0b` (Orange)
  - Danger: `#dc2626` (Red)

### Responsive Design
- Mobile-friendly sidebar navigation
- Responsive tables
- Touch-optimized buttons

### User Experience
- Loading states for all async operations
- Clear success/error messages
- Intuitive navigation with icons
- Modal dialogs for detailed views

## Making Existing Users Admins

To promote an existing user to admin:

**Method 1: Using Python script**
```bash
python create_admin.py
# Enter the existing username when prompted
# Choose 'yes' when asked to make them admin
```

**Method 2: Direct Database Update**
```sql
-- SQLite
UPDATE users SET is_admin = 1 WHERE username = 'your_username';
```

## Troubleshooting

### "Access denied. Admin privileges required"
- Ensure your user account has `is_admin=True`
- Check database: `SELECT username, is_admin FROM users;`
- Re-run create_admin.py to set admin flag

### Cannot see statistics
- Check backend logs for errors
- Verify JWT token in browser localStorage
- Ensure database connection is working

### Admin page not loading
- Clear browser cache
- Check browser console for JavaScript errors
- Verify `/admin` route is working: visit `/health` endpoint

## Best Practices

1. **Create Limited Admins**: Only give admin access to trusted team members
2. **Regular Monitoring**: Check platform statistics weekly
3. **User Privacy**: View chat histories only when necessary for support
4. **Backup Data**: Regular database backups before bulk operations
5. **Secure Passwords**: Use strong passwords for admin accounts

## Future Enhancements

Potential additions:
- [ ] Export user data to CSV
- [ ] Bulk user operations
- [ ] Advanced filtering and search
- [ ] User activity analytics
- [ ] Message content moderation
- [ ] Admin activity logs
- [ ] Email notifications for admin actions

## Support

For issues or questions:
- Check application logs in terminal
- Review browser console for frontend errors
- Contact: nawabkh2040@gmail.com

---

**SwasthAI Admin Panel** - Making healthcare management accessible and efficient! 🏥
