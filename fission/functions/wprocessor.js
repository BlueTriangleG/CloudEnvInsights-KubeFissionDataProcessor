module.exports = async function (context) {
  console.log(`Processed a weather observation`);
  return {
    status: 200,
    body: JSON.stringify (context.request.body.observations.data.map ((obs) => {
        const f = (i, n) => {
          return obs.aifstime_utc.substring (i, i + n);
        };
        const ts= `${f (0, 4)}-${f (4, 2)}-${f (6, 2)}T${f (8, 2)}:${f (10, 2)}:00Z`;
        return {
          stationid: `${obs.wmo}`,
          name: obs.name,
          geo: [obs.lon, obs.lat],
          local_date_time: obs.local_date_time,
          timestamp: ts,
          air_temp: obs.air_temp,
          rel_hum: obs.rel_hum
        };
      }
    ))
  };
}
