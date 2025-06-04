import React from 'react';
import styles from '../styles/InputSection.module.css';

const InputSection = ({ input, setInput, handleSendMessage, isLoading }) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className={styles.inputSection}>
      <textarea
        className={styles.inputField}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Ask me anything..."
        rows={1}
        disabled={isLoading}
      />
      <button 
        className={styles.sendButton} 
        onClick={handleSendMessage}
        disabled={isLoading || input.trim() === ''}
        aria-label="Send message"
      >
        {isLoading ? (
          <span className={styles.loadingDots}>
            <span className={styles.dot}></span>
            <span className={styles.dot}></span>
            <span className={styles.dot}></span>
          </span>
        ) : (
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        )}
      </button>
    </div>
  );
};

export default InputSection;
