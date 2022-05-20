(async (country, colors) => {

    const topology = await fetch(
        'https://code.highcharts.com/mapdata/countries/' + country + '/ch-all.topo.json'
    ).then(response => response.json());

    // Instantiate the map
    Highcharts.mapChart('container', {
        chart: {
            map: topology,
            spacingBottom: 20
        },

        title: {
            text: '{{country}}'
        },

        accessibility: {
            series: {
                descriptionFormat: 'Timezone {series.name} with {series.points.length} countries.'
            },
            point: {
                valueDescriptionFormat: '{point.name}.'
            }
        },

        legend: {
            enabled: true
        },

        plotOptions: {
            map: {
                allAreas: false,
                joinBy: ['postal-code', 'code'],
                dataLabels: {
                    enabled: true,
                    color: '#454545',
                    style: {
                        fontWeight: 'bold'
                    },
                    // Only show dataLabels for areas with high label rank
                    format: null,
                    formatter: function () {
                        if (
                            this.point.properties &&
                            this.point.properties.labelrank.toString() < 5
                        ) {
                            return this.point.properties['postal-code'];
                        }
                    }
                },
                tooltip: {
                    headerFormat: '',
                    pointFormat: '{point.name}: <b>{series.name}</b>'
                }
            }
        },

        series: [{
            name: 'UTC',
            data: [
                'ZH',
'BE',
'LU',
'UR',
'SZ',
'OW',
                'GE',
'NW',
'GL',
'ZG'
            ].map(code => ({ code }))
        }, {
            name: 'UTC + 1',
            data: [
                'FR',
'SO',
'BS',
'BL',
'SH',
'AR',
'AI',
'SG'
            ].map(code => ({ code }))
        }, {
            name: 'UTC + 2',
            data: [
                'GR',
'AG',
'TG',
'TI',
'VD',
'VS',
'NE',
'JU'

            ].map(code => ({ code }))
        }]
    });

})();