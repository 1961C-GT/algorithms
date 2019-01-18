function h = circle(ax,x,y,r)
d = r*2;
px = x-r;
py = y-r;
h = rectangle(ax,'Position',[px py d d],'Curvature',[1,1],...
    'LineStyle',':','EdgeColor',[0,0,1],'LineWidth',1.4);
daspect([1,1,1])