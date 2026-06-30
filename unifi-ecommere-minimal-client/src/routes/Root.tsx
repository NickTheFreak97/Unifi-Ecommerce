import { Link, Outlet } from "react-router";
import '../index.css'

export default function Root() {
  return (
    <div>
      <main>
        <Outlet />
      </main>
    </div>
  );
}
