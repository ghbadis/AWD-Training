const app = require('./app');
const { Eureka } = require('eureka-js-client');

const PORT = 8085;

// ===============================
// Configuration Eureka
// ===============================
const eureka = new Eureka({
  instance: {
    // Instance affichée dans Eureka
    instanceId: `localhost:meeting:${PORT}`,

    // Nom du microservice Eureka
    app: 'MEETING',

    hostName: 'localhost',
    ipAddr: '127.0.0.1',

    // Port du microservice
    port: {
      '$': PORT,
      '@enabled': true
    },

    // Adresse virtuelle du service
    vipAddress: 'MEETING',

    // Informations Data Center
    dataCenterInfo: {
      '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
      name: 'MyOwn'
    }
  },

  // ===============================
  // Eureka Server
  // ===============================
  eureka: {
    host: 'localhost',
    port: 8761,
    servicePath: '/eureka/apps/'
  }
});

// ===============================
// Démarrage du serveur Meeting
// ===============================
const server = app.listen(PORT, () => {
  console.log('======================================');
  console.log('MEETING Microservice');
  console.log(`URL : http://localhost:${PORT}`);
  console.log(`Swagger : http://localhost:${PORT}/swagger-ui`);
  console.log('======================================');

  // Enregistrement dans Eureka
  eureka.start((error) => {
    if (error) {
      console.error('Erreur lors de l\'enregistrement Eureka :', error);
    } else {
      console.log('MEETING registered in Eureka');
      console.log(`Instance : localhost:meeting:${PORT}`);
    }
  });
});

// ===============================
// Arrêt propre du microservice
// ===============================
process.on('SIGINT', () => {
  console.log('\nStopping MEETING...');

  eureka.stop(() => {
    console.log('MEETING unregistered from Eureka');

    server.close(() => {
      console.log('MEETING stopped');
      process.exit(0);
    });
  });
});