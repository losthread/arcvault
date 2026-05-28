import { Home, TrendingUp, Compass, Star, Computer, Pi, Settings, Menu} from "lucide-react";
import { useState } from "react";

const pages = ['Home', 'Popular', 'Explore'];
const pageLinks = ['/home', '/popular', '/explore'];
const icons = [Home, TrendingUp, Compass];
const favouriteCommunities = ['Computer Science', 'Mathematics', 'Engineering']
const communityLinks = ['Computer Science', 'Mathematics', 'Engineering']
const favouriteCommunitiesProfile = [Computer, Pi, Settings]

export default function Sidebar() {
const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <aside className={`relative flex flex-col lg:gap-8 bg-sidebar border-r border-sidebar-border h-screen lg:p-4 transition-all duration-500 ${isCollapsed ? 'lg:w-0' : 'lg:w-60'}`}>
      {/* Collapse Button On the border  */}
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className='absolute -right-4 top-8 bg-sidebar border border-sidebar-border rounded-full p-1 hover:bg-sidebar-accent transition ease-in'
        title={isCollapsed ? 'Expand' : 'Collapse'}
      >
        <Menu size={20} />
      </button>
      
      {/* Pages links */}
      <ul className={`flex flex-col lg:gap-2 transition-all duration-200 ${isCollapsed ? 'opacity-0 invisible' : 'opacity-100 visible'}`}>
        {pages.map((page, index) => {
          const Icon = icons[index];
          const link = pageLinks[index];
          return (
            <li key={page}>
              <a href={link} className='flex items-center lg:gap-3 lg:p-2 rounded hover:bg-sidebar-accent text-sidebar-foreground transition duration-300 ease-out'>
                <Icon size={24} />
                <span>{page}</span>
              </a>
            </li>
          )
        })}
      </ul>

      {/* Favorite Communities Section */}
      <div className={`transition-all duration-200 ${isCollapsed ? 'opacity-0 invisible' : 'opacity-100 visible'}`}>
        <h3 className='flex lg:gap-2 items-center lg:text-sm font-semibold text-muted-foreground lg:mb-3 lg:px-2'>
          <Star size={20}/>
          Favorite Communities
        </h3>
        <ul className='flex flex-col lg:gap-1'>
          {favouriteCommunities.map((community, index) => {
            const ProfilePic = favouriteCommunitiesProfile[index];
            const communityLink = communityLinks[index]
            return (
              <li key={community}>
                <a href={communityLink} className='flex items-center lg:gap-3 lg:p-2 rounded lg:text-sm text-sidebar-foreground hover:bg-sidebar-accent transition duration-300 ease-out'>
                  <ProfilePic size={20} />
                  <span>{community}</span>
                </a>
              </li>
            )
          })}
        </ul>
      </div>
    </aside>
  )
}