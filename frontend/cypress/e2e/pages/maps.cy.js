describe('Map Tests', () => {
  beforeEach(() => {
    cy.visit('/maps'); 
  });

  it('loads the map successfully', () => {
    cy.get('#map').should('be.visible');
  });

  it('gets current location and updates latitude and longitude fields', () => {
    // 模拟导航器的地理定位功能
    cy.window().then((win) => {
      cy.stub(win.navigator.geolocation, "getCurrentPosition").callsFake((cb) => {
        return cb({ coords: { latitude: 53.3437935, longitude: -6.254571599999999 } });
      });
    });

    cy.get('button').contains('Get Current Location').click();
    cy.get('#latitude').should('have.value', '53.34379'); 
    cy.get('#longitude').should('have.value', '-6.25457'); 
  });

  it('geocodes address and updates latitude and longitude fields', () => {

    cy.window().then((win) => {
      // 模拟 geocoder 对象
      const mockGeocoder = {
        geocode: (request, callback) => {
          const results = [{
            formatted_address: '模拟的地址',
            geometry: {
              location: {
                lat: () => 53.34379,
                lng: () => -6.25457,
              }
            }
          }];
          callback(results, google.maps.GeocoderStatus.OK);
        }
      };
      // 替换 window.google.maps.Geocoder 对象
      cy.stub(win.google.maps, 'Geocoder').returns(mockGeocoder);
    });

    const address = 'Trinity College Dublin';
    cy.get('#address').type(address);
    cy.get('button').contains('Geocode Address').click();
    
    cy.get('#address').should('have.value', address) 
    // 使用更长的超时时间确保异步操作有足够的时间完成
    cy.get('#latitude', { timeout: 50000 }).should('have.value', '53.34379');
    cy.get('#longitude', { timeout: 50000 }).should('have.value', '-6.25457');

  });

  
});
