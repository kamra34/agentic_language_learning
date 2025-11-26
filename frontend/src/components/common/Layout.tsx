import { Outlet, Link, useLocation } from 'react-router-dom';
import { Home, BookOpen, MessageSquare, User, GraduationCap } from 'lucide-react';
import { clsx } from 'clsx';

const navItems = [
  { path: '/', icon: Home, label: 'Home' },
  { path: '/vocabulary', icon: BookOpen, label: 'Vocab' },
  { path: '/grammar', icon: GraduationCap, label: 'Grammar' },
  { path: '/chat', icon: MessageSquare, label: 'Chat' },
  { path: '/profile', icon: User, label: 'Profile' },
];

export function Layout() {
  const location = useLocation();

  return (
    <div className="min-h-screen flex flex-col">
      {/* Main content */}
      <main className="flex-1 pb-20 safe-bottom">
        <Outlet />
      </main>

      {/* Bottom navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 safe-bottom">
        <div className="flex justify-around items-center h-16">
          {navItems.map(({ path, icon: Icon, label }) => {
            const isActive = location.pathname === path;
            return (
              <Link
                key={path}
                to={path}
                className={clsx(
                  'flex flex-col items-center justify-center w-full h-full transition-colors',
                  isActive ? 'text-primary-600' : 'text-gray-500 hover:text-gray-700'
                )}
              >
                <Icon className="w-6 h-6" />
                <span className="text-xs mt-1">{label}</span>
              </Link>
            );
          })}
        </div>
      </nav>
    </div>
  );
}

export default Layout;
