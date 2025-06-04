import React, { useEffect, useState } from 'react';
import styles from '../styles/SplashScreen.module.css';

const SplashScreen = ({ onFinished }) => {
  const [fadeOut, setFadeOut] = useState(false);

  useEffect(() => {
    // Start fade out animation after 2 seconds
    const timer = setTimeout(() => {
      setFadeOut(true);
    }, 2000);

    // Complete splash screen after animation duration (2.5 seconds total)
    const completeTimer = setTimeout(() => {
      onFinished();
    }, 2500);

    return () => {
      clearTimeout(timer);
      clearTimeout(completeTimer);
    };
  }, [onFinished]);

  return (
    <div className={`${styles.splashScreen} ${fadeOut ? styles.fadeOut : ''}`}>
      <div className={styles.content}>
        <div className={styles.logo}>
          <span className={styles.logoText}>RIT</span>
          <span className={styles.logoTextSecondary}>Buddy</span>
        </div>
        <div className={styles.tagline}>Your AI Campus Assistant</div>
        <div className={styles.loadingBar}>
          <div className={styles.loadingProgress}></div>
        </div>
      </div>
    </div>
  );
};

export default SplashScreen;
