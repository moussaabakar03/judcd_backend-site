import { Link } from 'react-router-dom';
import { ASSETS, ASSOCIATION } from '@utils/constants';

const menuItems = [
  { path: '/admin/dashboard', label: 'Tableau de bord', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
  { path: '/admin/galerie', label: 'Galerie', icon: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z' },
  { path: '/admin/blog', label: 'Blog', icon: 'M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z' },
  { path: '/admin/messages', label: 'Messages', icon: 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' },
  { path: '/admin/dons', label: 'Dons', icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z' },
  { path: '/admin/adhesions', label: 'Adhesions', icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z' },
];

export default function AdminSidebar({ currentPath, onLogout }) {
  return (
    <aside className="fixed top-0 left-0 h-full w-60 lg:w-64 bg-[#002060] text-white z-30 hidden lg:flex flex-col">
      <div className="p-5 lg:p-6 border-b border-white/10">
        <Link to="/admin/dashboard" className="flex items-center gap-3">
          <img src={ASSETS.logo} alt={ASSOCIATION.name} className="h-9 lg:h-10 w-auto brightness-0 invert" />
          <div>
            <span className="font-heading font-bold text-sm block leading-tight">Admin {ASSOCIATION.name}</span>
            <span className="text-white/40 text-[10px]">Panel de gestion</span>
          </div>
        </Link>
      </div>
      <nav className="flex-1 p-3 lg:p-4 space-y-1 overflow-y-auto">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={lex items-center gap-3 px-3 lg:px-4 py-2.5 lg:py-3 rounded-xl text-sm font-medium transition-all \}
          >
            <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} />
            </svg>
            <span className="truncate">{item.label}</span>
          </Link>
        ))}
      </nav>
      <div className="p-3 lg:p-4 border-t border-white/10">
        <button onClick={onLogout} className="flex items-center gap-3 px-3 lg:px-4 py-2.5 lg:py-3 rounded-xl text-sm font-medium text-white/70 hover:bg-white/10 hover:text-white transition-all w-full">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          Deconnexion
        </button>
      </div>
    </aside>
  );
}
