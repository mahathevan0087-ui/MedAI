import { NavLink } from 'react-router-dom'
import styles from './Navbar.module.css'

export default function Navbar() {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <NavLink to="/" className={styles.brand}>
          <span className={styles.dot} /> MedAI+
        </NavLink>
        <nav className={styles.nav}>
          <NavLink to="/" end className={({ isActive }) => isActive ? styles.active : styles.link}>Home</NavLink>
          <a href="#features" className={styles.link}>Features</a>
          <a href="#workflow" className={styles.link}>How It Works</a>
          <NavLink to="/about" className={({ isActive }) => isActive ? styles.active : styles.link}>About</NavLink>
          <NavLink to="/contact" className={({ isActive }) => isActive ? styles.active : styles.link}>Contact</NavLink>
          <NavLink to="/login" className={styles.login}>Login</NavLink>
        </nav>
      </div>
    </header>
  )
}
