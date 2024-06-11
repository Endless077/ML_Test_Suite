// Footer
import React from 'react';
import { MDBFooter } from 'mdb-react-ui-kit';

export default function Footer() {
  return (
    <MDBFooter bgColor='light' className='text-center text-lg-left'>
      <div className='text-center p-3' style={{ backgroundColor: 'rgba(0, 0, 0, 0.2)' }}>
        &copy; {new Date().getFullYear()} a GNU General Public License:{' '}
        <a className='text-dark' href='https://github.com/Endless077/ML_Security_Project'>
          ML Suite Test
        </a>
        <div>
          Powered by{' '}
          <a className='text-dark' href='https://github.com/Endless077/'>
            A. Garofalo
          </a>{' '}
          and{' '}
          <a className='text-dark' href='https://github.com/Fulvioserao99'>
            F. Serao
          </a>
        </div>
        <div>All Right Reserved.</div>
      </div>
    </MDBFooter>
  );
}
