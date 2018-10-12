define([
    'underscore',
    'knockout',
    'viewmodels/report',
    'reports/potree/potree-setup',
    'arches',
    'knockstrap',
    'bindings/chosen',
], function (_, ko, ReportViewModel, potreeSetup) {
    return ko.components.register('potree-report', {
        viewModel: function (params) {
            var self = this;
            params.configKeys = ['nodes'];
            ReportViewModel.apply(this, [params]);

            self.potreeZipFiles = ko.observableArray([]);

            if (self.report.get('tiles')) {
                var potreeZipFiles = [];
                self.report.get('tiles').forEach(function (tile) {
                    _.each(tile.data, function (val) {
                        if (Array.isArray(val)) {
                            val.forEach(function (item) {

                                if (item.status &&
                                    (item.name.split('.').pop() == 'zip')) {
                                    potreeZipFiles.push({
                                        src: item.url,
                                        name: item.name
                                    });
                                }
                            });
                        }
                    }, self);
                }, self);

                if (potreeZipFiles.length > 0) {
                    self.potreeZipFiles(potreeZipFiles);
                    let modelName = potreeZipFiles[0].name;
                    let filepath = potreeZipFiles[0].src;
                    let filepathWithoutExtension = "";
                    if (filepath !== undefined) {
                        filepathWithoutExtension = filepath.replace(/\.[^/.]+$/, "");
                    }
                    window.viewer = new Potree.Viewer(document.getElementById("potree_render_area"));
                    potreeSetup.setupPotree(filepathWithoutExtension + "/cloud.js", modelName)
                }
            }

            var widgets = [];
            var getCardWidgets = function (card) {
                widgets = widgets.concat(card.model.get('widgets')());
                card.cards().forEach(function (card) {
                    getCardWidgets(card);
                });
            };
            ko.unwrap(self.report.cards).forEach(getCardWidgets);

            this.nodeOptions = ko.observableArray(
                widgets.map(function (widget) {
                    return widget.node
                }).filter(function (node) {
                    return ko.unwrap(node.datatype) === 'file-list';
                })
            );
        },
        template: {
            require: 'text!report-templates/potree'
        }
    });
});