define([
    'underscore',
    'knockout',
    'knockout-mapping',
    'viewmodels/report',
    'arches',
    'pannellum'
], function(_, ko, koMapping, ReportViewModel, arches) {
    return ko.components.register('360-image-report', {
        viewModel: function(params) {
            var self = this;
            params.configKeys = ['nodes'];
            ReportViewModel.apply(this, [params]);

            self.imgs = ko.computed(function() {
                var imgs = [];
                var nodes = self.nodes();
                self.tiles().forEach(function(tile) {
                    _.each(tile.data, function(val, key) {
                        val = koMapping.toJS(val);
                        if (Array.isArray(val)) {
                            val.forEach(function(item) {
                                if (item.status &&
                                    item.type &&
                                    item.status === 'uploaded' &&
                                    item.type.indexOf('image') > -1 &&
                                    _.contains(nodes, key)
                                ) {
                                    imgs.push({
                                        src: item.url,
                                        alt: item.name
                                    });
                                }
                            });
                        }
                    }, self);
                }, self);
                if (imgs.length === 0) {
                    imgs = [{
                        src: arches.urls.media + 'img/photo_missing.png',
                        alt: ''
                    }];
                }
                return imgs;
            });

            if (self.imgs().length > 0) {
                window.pannellum.viewer('panorama', {
                    "type": "equirectangular",
                    "panorama": self.imgs()[0].src,
                    "autoLoad": true
                })
            }
        },
        template: {
            require: 'text!report-templates/three-sixty-image'
        }
    });
});