function hw01_plot(name,x,Y,eventX,eventY,band,plotTitle)
% Refresh the existing Typst data and show equivalent MATLAB curves.
% Y and eventY use the display units specified by the figure's axis label.
cfg = hw01_settings();
path = fullfile(cfg.dataDirectory,[name '.json']);
d = jsondecode(fileread(path));
x = x(:)';
assert(size(Y,2)==numel(x) && all(isfinite(Y),'all'));
assert(size(Y,1)==numel(d.curves));
assert(numel(eventX)==numel(d.events));
d.x = x;
d.xlim = [x(1) x(end)];
d.band = band;
if nargin==7
    d.title = plotTitle;
end
span = max(Y,[],'all')-min(Y,[],'all');
if span==0, span=max(1,abs(Y(1))); end
upperMargin = 0.13+0.25*~isempty(eventX);
d.ylim = [min(Y,[],'all')-0.13*span, ...
    max(Y,[],'all')+upperMargin*span];
figure('Name',d.title,'Color','w');
hold on
styles = {'-','--','-.'};
for j=1:size(Y,1)
    d.curves(j).y = Y(j,:);
    plot(x,Y(j,:),styles{mod(j-1,numel(styles))+1}, ...
        'Color',cfg.colors(mod(j-1,size(cfg.colors,1))+1,:), ...
        'LineWidth',1.2,'DisplayName',d.curves(j).label);
end
if ~isempty(band)
    yline(band,':k','HandleVisibility','off');
    yline(-band,':k','HandleVisibility','off');
end
for j=1:numel(eventX)
    d.events(j).x = eventX(j);
    d.events(j).y = eventY(j);
    d.events(j).value = sprintf('(%.4g, %.4g)',eventX(j),eventY(j));
    point = plot(eventX(j),eventY(j),'ks','HandleVisibility','off');
    datatip(point,eventX(j),eventY(j));
end
xlabel(d.xlabel); ylabel(d.ylabel); title(d.title);
grid on; box on; xlim(d.xlim); ylim(d.ylim);
if size(Y,1)>1, legend('Location','best'); end
fid = fopen(path,'w');
assert(fid~=-1,'Cannot write figure data.');
cleanup = onCleanup(@() fclose(fid));
d.curves = num2cell(d.curves);
d.events = num2cell(d.events);
payload = jsonencode(d);
% Typst represents an absent settling band as none, rather than an array.
payload = strrep(payload,'"band":[]','"band":null');
fprintf(fid,'%s\n',payload);
end
