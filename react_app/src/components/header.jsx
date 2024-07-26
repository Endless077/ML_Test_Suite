// Header
import React from 'react';
import {
  MDBContainer,
  MDBNavbar,
  MDBNavbarBrand,
  MDBNavbarItem,
  MDBNavbarLink,
  MDBDropdown,
  MDBDropdownToggle,
  MDBDropdownMenu,
  MDBDropdownItem
} from 'mdb-react-ui-kit';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

export default function Navbar(props) {
  return (
    <>
      <MDBNavbar light bgColor='light'>
        <MDBContainer fluid>
          <MDBNavbarBrand href='/homepage'>
            <img
              src='/assets/art_logo.png'
              height='60'
              alt='Art Logo'
              loading='lazy'
            />
            ML Test Suite
          </MDBNavbarBrand>
          <div style={{
            textAlign: 'center',
            flex: 1,
            fontSize: '36px',
            fontWeight: 'bold',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            marginLeft: '100px'
          }}>
            {props.pageTitle}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', marginRight: '33px' }}>
            <MDBNavbarItem style={{ marginRight: '30px', listStyleType: 'none' }}>
              <MDBDropdown>
                <MDBDropdownToggle tag='a' className='nav-link' role='button'>
                  Attacks
                </MDBDropdownToggle>
                <MDBDropdownMenu style={{ borderRadius: '0', boxShadow: '0 2px 5px rgba(0,0,0,0.1)' }}>
                  <MDBDropdownItem><Link to='/attack/FGM' style={{ color: 'black' }}>Evasion - First Gradient Method</Link></MDBDropdownItem>
                  <hr className="dropdown-divider" />
                  <MDBDropdownItem><Link to='/attack/PGD' style={{ color: 'black' }}>Evasion - Projected Gradient Descent</Link></MDBDropdownItem>
                  <hr className="dropdown-divider" />
                  <MDBDropdownItem><Link to='/attack/CopycatCNN' style={{ color: 'black' }}>Extraction - CopycatCNN</Link></MDBDropdownItem>
                  <hr className="dropdown-divider" />
                  <MDBDropdownItem><Link to='/attack/MIFace' style={{ color: 'black' }}>Inference - MIFace</Link></MDBDropdownItem>
                  <hr className="dropdown-divider" />
                  <MDBDropdownItem><Link to='/attack/CleanLabelBackdoor' style={{ color: 'black' }}>Poisoning - Clean Label Backdoor</Link></MDBDropdownItem>
                  <hr className="dropdown-divider" />
                  <MDBDropdownItem><Link to='/attack/SimpleBackdoor' style={{ color: 'black' }}>Poisoning - Simple Backdoor</Link></MDBDropdownItem>
                </MDBDropdownMenu>
              </MDBDropdown>
            </MDBNavbarItem>

            <MDBNavbarItem style={{ marginRight: '30px', listStyleType: 'none' }}>
              <MDBDropdown>
                <MDBDropdownToggle tag='a' className='nav-link' role='button'>
                  Defences
                </MDBDropdownToggle>
                <MDBDropdownMenu style={{ borderRadius: '0', boxShadow: '0 2px 5px rgba(0,0,0,0.1)' }}>
                  <MDBDropdownItem><Link to='/defense/ActivationDefense' style={{ color: 'black' }}>Detector - Activation Defense</Link></MDBDropdownItem>
                  <hr className="dropdown-divider" />
                  <MDBDropdownItem><Link to='/defense/ReverseSigmoid' style={{ color: 'black' }}>Post Processor - Reverse Sigmoid</Link></MDBDropdownItem>
                  <hr className="dropdown-divider" />
                  <MDBDropdownItem><Link to='/defense/TotalVarMin' style={{ color: 'black' }}>Pre Processor - TotalVarMin</Link></MDBDropdownItem>
                  <hr className="dropdown-divider" />
                  <MDBDropdownItem><Link to='/defense/AdversarialTrainer' style={{ color: 'black' }}>Trainer - Adversarial Trainer</Link></MDBDropdownItem>
                  <hr className="dropdown-divider" />
                  <MDBDropdownItem><Link to='/defense/STRongIntentionalPerturbation' style={{ color: 'black' }}>Transformer - STRong Intentional Pertubation</Link></MDBDropdownItem>
                </MDBDropdownMenu>
              </MDBDropdown>
            </MDBNavbarItem>

            <MDBNavbarItem style={{ marginRight: '30px', listStyleType: 'none' }}>
              <Link to='/login' style={{ color: 'var(--mdb-nav-link-color)' }}>Profile</Link>
            </MDBNavbarItem>

            <MDBNavbarItem style={{ listStyleType: 'none' }}>
              <MDBNavbarLink href='https://github.com/Endless077/ML_Security_Project' target='_blank'>
                About
              </MDBNavbarLink>
            </MDBNavbarItem>
          </div>
        </MDBContainer>
      </MDBNavbar>
    </>
  );
}

Navbar.propTypes = {
  pageTitle: PropTypes.string.isRequired,
};
