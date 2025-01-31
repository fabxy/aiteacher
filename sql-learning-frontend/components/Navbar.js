"use client";
import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-blue-600 p-4 text-white shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-lg font-bold">
          SQL Learning
        </Link>
        
        <button onClick={() => setIsOpen(!isOpen)} className="md:hidden">
          ☰
        </button>

        <ul className={`md:flex space-x-6 ${isOpen ? "block" : "hidden"} md:block`}>
          <li>
            <Link href="/" className={pathname === "/" ? "underline" : ""}>Home</Link>
          </li>
          <li>
            <Link href="/lessons" className={pathname === "/lessons" ? "underline" : ""}>Lessons</Link>
          </li>
          <li>
            <Link href="/sql-editor" className={pathname === "/sql-editor" ? "underline" : ""}>SQL Editor</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}
