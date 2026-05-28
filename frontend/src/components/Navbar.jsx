import { Plus, Search, Bell, User } from 'lucide-react';
import { Input } from './ui/input';
import { Button } from './ui/button';

export default function Navbar() {
  return (
    <header className='flex lg:gap-60 items-center justify-between lg:px-8 lg:py-3 bg-card border-b border-border'>
      <div className='lg:text-xl font-bold text-foreground'>
        <a href='#'>ArcVault</a>
      </div>

      <div className='flex-1 lg:mx-4 relative'>
        <Input placeholder='Search resources...' className='lg:px-5 lg:py-4.5 rounded-3xl'/>
        <Search className='absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none' size={18} />
      </div>

      <div className='flex items-center gap-3'>
        <Button size='default'>
          <Plus />
          New
        </Button>
        
        <Button size='icon-lg' className='rounded-full'>
          <Bell />
        </Button>

        <Button size='icon-lg' className='rounded-full'>
          <User />
        </Button>
      </div>
    </header>
  )
}