% Use the associative.trace data to generate a plot
% which illustrates the effect of associativity on hit
% rate (going up as we move towards FA)
% Hold the other variables constant

clear; clc; clf

%Use cache size 1024, block size 8 and WT

x = [8, 16, 32, 128]
y = [0.1, 0.2, 0.2, 0.2]
plot(x, y)
xlabel('Block Size (Bytes)')
ylabel('Hit Rate')

% neworder = {
%     'DM'            [0.16]
%     '2W'            [0.31]
%     '4W'            [0.56]
%     'FA'            [0.75]}
% 
% plot([neworder{:,2}])
% set(gca,'xticklabel',neworder(:,1))

% x = ['D', '2', '4', 'F']
% y = [0.16, 0.31, 0.56, 0.75]
% 
% plot(y)
% set(gca,'xticklabel',x.')
