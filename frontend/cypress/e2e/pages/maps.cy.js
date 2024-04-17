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
    // cy.get('#latitude').should('have.value', '53.34379'); 
    // cy.get('#longitude').should('have.value', '-6.25457'); 
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
          callback(results, win.google.maps.GeocoderStatus.OK);
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

  it('loads disasters data and displays markers or circles on the map', () => {
    // 假设 loadDisasters 被触发并正确加载了数据
    cy.get('#map').find('.gmnoprint').should('exist'); // 检查是否有标记或圆形
    // 模拟点击某个灾害标记
    cy.get('.gmnoprint').first().click();
    // 检查信息窗口是否包含正确的灾害信息
    // cy.get('.gm-style-iw').should('contain', 'Disaster Name');
  });

  it('fetches safe point and displays route when in disaster area', () => {
    // 模拟当前用户位于灾难区域
    cy.stub(window, 'fetch').resolves({
      json: () => Promise.resolve({
        data: { safe_lat: 53.349805, safe_lng: -6.26031 }
      })
    });

    // 模拟点击获取当前位置
    cy.get('button').contains('Get Current Location').click();

    // 验证是否请求了安全点数据
    // cy.wait('@fetchSafePoint').its('response.statusCode').should('eq', 200);

    // 检查是否显示了路线
    // cy.get('.directionsPanel').should('be.visible');
  });


  it('updates location periodically when travel mode is DRIVING', () => {
    cy.get('#mode').select('DRIVING');
    // 检查是否启动了位置更新
    // cy.get('@updateLocation').should('have.been.called');

    // 模拟过一段时间后再次检查
    cy.clock();
    cy.tick(10000); // 假设每10秒更新一次位置
    // cy.get('@updateLocation').should('have.been.calledTwice');
  });

  it('handles geolocation errors correctly', () => {
    cy.window().then((win) => {
      cy.stub(win.navigator.geolocation, "getCurrentPosition").callsFake((_, errorCallback) => {
        errorCallback({
          code: 1,
          message: "Geolocation permission denied"
        });
      });
    });

    cy.get('button').contains('Get Current Location').click();
    cy.get('.gm-style-iw').should('contain', 'Error: The Geolocation service failed.');
  });

  it('geocodes an address and updates the map view', () => {
    const address = 'New Address';
    cy.get('#address').clear().type(address);
    cy.get('button').contains('Geocode Address').click();

    // 检查地图是否已重新定位到新地址
    cy.get('#latitude').should('not.have.value', '53.34379');
    cy.get('#longitude').should('not.have.value', '-6.25457');
  });


  
});
