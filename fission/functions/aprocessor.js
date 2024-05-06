module.exports = async function (context) {
  console.log(`Processed an air quality observation`);
  return {
    status: 200,
    body: JSON.stringify (context.request.body.features.map ((feat) => {
        return [{
          stationid: feat.properties.site_id,
          name: feat.properties.site_name,
          geo: [feat.properties.longitude, feat.properties.latitude],
          timestamp: feat.properties.time_stamp,
          pm10: feat.properties.pm10,
          pm2p5:feat.properties.pm2p5,
          ozone:feat.properties.ozone
        }];
      }
    ))
  };
}
