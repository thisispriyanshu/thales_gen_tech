"use client";

import { NAV_LINKS } from "@/constants";
import { usePathname } from "next/navigation";
import Link from "next/link";
import Button from "@/components/Button";

const Navbar = () => {
  const pathname = usePathname();

  return (
    <nav className="flex justify-between items-center p-4 bg-gray-900 text-white">
      {/* Left: Website Logo/Name */}
      <div className="flex items-center space-x-2">
        <span className="text-2xl">🔍</span>
        <Link href="/">
          Deepfake Detector
        </Link>
      </div>

      {/* Right: Navigation Links */}
      <ul className="flex space-x-6">
        {NAV_LINKS.map((link) => (
          <li key={link.path}>
            <Link href={link.path}>
              
                {link.label}
          
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Navbar;
