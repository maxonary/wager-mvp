import React from 'react';

const PAYPAL_DONATION_URL = process.env.REACT_APP_PAYPAL_DONATION_URL;

const DonationButton = () => {
  const handleButtonClick = () => {
    window.open(PAYPAL_DONATION_URL, '_blank');
  };

  return (
    <button
      onClick={handleButtonClick}
      style={{
        padding: '10px 20px',
        backgroundColor: '#0070ba',
        color: '#ffffff',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        fontSize: '16px'
      }}
    >
       Add balance via PayPal
    </button>
  );
};

export default DonationButton;