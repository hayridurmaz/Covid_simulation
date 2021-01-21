clear all;
day = 500;
dti = 5;
c(1:75) = 10;
c(75:125) = 2;
c(125:250) = 2;
c(250:375) = 6;
c(375:500)=1;

%c(25) = 10;
T = 0.03;
dts = 6;
ps = 0.6;
dtr = 10;
z = ones(1,day);
s = zeros(1,day);
a = zeros(1,day);
i = zeros(1,day);
% z(1,1:17) = [1,2,7,15,22,34,41,56,63,78,91,108,110,123,134,155,169];
z(1,25) = 25;
tot_pop = 8e6;
sum_s = zeros(1,day);
sum_a = zeros(1,day);
sum_v = zeros(1,day);
norm_par = zeros(1,day);
v = zeros(1,day);
p1 = 0.8;
p2 = 0.95;
p3 = 0.7;
for t = 25:day
     %norm_par(t) = (1-z(t)/(tot_pop-sum_s(t)*p1-sum_a(t)*p2-sum_v(t)*p3));
     %c(t) = c(t)* norm_par(t);
    s(t) = z(t-dti-dts)*ps*c(t-dti-dts)*T;
    a(t) = z(t-dti-dtr)*(1-ps)*c(t-dti-dtr)*T;
    i(t) = z(t-dti)*c(t-dti)*T;
    z(t+1) = z(t)+ i(t)-s(t)-a(t);
    sum_s(t) = sum_s(t) + s(t);
    sum_a(t) = sum_a(t) + a(t);
    sum_v(t) = sum_v(t) + v(t);
end
plot(z);
title('Two different peaks according to c parameter');
xlabel('[Days]') 
ylabel('[Number of Covid Cases]') 
% figure();
% plot(z_case);
% figure();
% plot(conf_case(17:100));