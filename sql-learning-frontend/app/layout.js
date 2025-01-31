export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-100 text-gray-900">
        <Navbar />
        <main className="p-6 max-w-4xl mx-auto">{children}</main>
      </body>
    </html>
  );
}

// Import the Navbar component
import Navbar from "../components/Navbar";
