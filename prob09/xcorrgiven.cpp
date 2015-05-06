#include<vector>
#include<cmath>
#include<iostream>
#include<iomanip>

#define MIN(X,Y) ((X) < (Y) ? (X) : (Y))
#define MAX(X,Y) ((X) < (Y) ? (Y) : (X))
#define THRESCORR 1e-30
#define MAX_WAVE_SIZE 3010
#define MIN_INF -1e30

std::vector<double> crosscorr(const double* x, int xSize, const double * y, int ySize)
{
	std::vector<double> xcorr;

	//! Calculate the mean of the two series x[], y[]
	double xMean = 0.0;
	for (int i = 0; i < xSize; i++) {
	    if (x[i] >= 0.0 && x[i] <= 15.0)
		xMean += x[i] / xSize;
	}

	double yMean = 0.0;
	for (int i = 0; i < ySize; i++) {
	    if (y[i] >= 0.0 && y[i] <= 15.0)
		yMean += y[i] / ySize;
	}

	//! Calculate the denominator (product of standard deviations)
	double xSumCuadraticDiff = 0.0;
	for (int i = 0; i < xSize; i++) {
		xSumCuadraticDiff += pow(x[i] - xMean, 2);
	}

	double ySumCuadraticDiff = 0.0;
	for (int i = 0; i < ySize; i++) {
		ySumCuadraticDiff += pow(y[i] - yMean, 2);
	}

	double denom = sqrt(xSumCuadraticDiff * ySumCuadraticDiff);
	if (denom < THRESCORR){
		xcorr.resize(0);
		return xcorr;
	}

	//! Calculate the correlation series
	xcorr.resize(ySize - xSize + 1);

	for (int delay = 0; delay < xcorr.size(); delay++) {
		double xySum = 0.0;
		for (int i = 0; i < xSize; i++) {
			xySum += (x[i] - xMean) * (y[i + delay ] - yMean);
		}

		xcorr[delay] = xySum / denom;
	}
	return xcorr;
}

double findScore(const double* wave, int waveSize, const double* pattern, int patternSize){
	double score = 0.0;
	int minSubvectorLength = 2;

	for (int subvectorStart = 0; subvectorStart <= waveSize - minSubvectorLength; subvectorStart++) {
		for (int subvectorLength = minSubvectorLength; subvectorLength <= MIN(waveSize - subvectorStart, patternSize); subvectorLength++) {
			std::vector<double> xcorrelation = crosscorr(&(wave[subvectorStart]), subvectorLength, pattern, patternSize);

			for (int xcorrelationIndex = 0; xcorrelationIndex < xcorrelation.size(); xcorrelationIndex++) {
				score = MAX(score, xcorrelation[xcorrelationIndex] * subvectorLength);
			}
    		}
	}

	return score;
}

// Store cumSum of source in target
void cumSum(const double* source, int sourceSize, double* target) {
	target[0] = 0.0;
	for (int i = 0; i < sourceSize; i++) {
		target[i+1] = target[i] + source[i];
	}
}

// Store cumSum of squared elements of source in target
void cumSum2(const double* source, int sourceSize, double* target) {
	target[0] = 0.0;
	for (int i = 0; i < sourceSize; i++) {
		target[i+1] = target[i] + (source[i] * source[i]);
	}
}

// Store the cumSum of elementwise multiplication for each possible delay
void cumUncorrectedCrossCorr(const double* x, int xSize, const double* y, int ySize, double target[][MAX_WAVE_SIZE], int maxDelay, int maxNegDelay) {
	for (int d = -maxNegDelay; d <= maxDelay; d++) {
		int dx = (d < 0) ? maxDelay - d : d;
		target[dx][MAX(0, -d)] = 0.0;
		for (int i = MAX(0, -d); i < xSize && i+d < ySize; i++) {
			target[dx][i+1] = target[dx][i] + x[i] * y[i+d];
		}
	}
}

// Computes sum of squared differences for a vector x
double computeSumSquaredDif(const double* cum_x, const double* cum_x2, int xStart, int xLength, double xMean) {
	return (cum_x2[xLength+xStart] - cum_x2[xStart]) + xLength * xMean * xMean - 2 * xMean * (cum_x[xLength+xStart] - cum_x[xStart]);
}

double computeCrossCorrCoef(const double cum_xy[][MAX_WAVE_SIZE], const double* cum_x, const double* cum_y, int xStart, int xLength, int delay, double xMean, double yMean, int global_max_delay) {
	delay -= xStart;
	int dx = (delay < 0) ? global_max_delay - delay : delay;
    return xLength * xMean * yMean + (cum_xy[dx][xStart+xLength] - cum_xy[dx][xStart]) - yMean * (cum_x[xStart+xLength] - cum_x[xStart]) - xMean * (cum_y[delay+xStart+xLength] - cum_y[delay+xStart]);
}

// Returns the maximum cross correlation value for the specified subvector with the pattern (without multiplying by the vector length)
double maxCrossCorrHardcore(const double cum_wp[][MAX_WAVE_SIZE], const double* cum_w, const double* cum_p, const double* cum_w2, const double* cum_p2,
	int subvectorStart, int subvectorLength, int patternSize, int global_max_delay) {
	double xMean = (cum_w[subvectorLength+subvectorStart] - cum_w[subvectorStart]) / subvectorLength;
	double yMean = (cum_p[patternSize] - cum_p[0]) / patternSize; // no need to recompute but it's O(1)
	double x_ssd = computeSumSquaredDif(cum_w, cum_w2, subvectorStart, subvectorLength, xMean);
	double y_ssd = computeSumSquaredDif(cum_p, cum_p2, 0, patternSize, yMean);
	double denom = sqrt(x_ssd * y_ssd);
	if (denom < THRESCORR){
		return 0;
	}
	int maxDelay = patternSize - subvectorLength;
	double maxValue = MIN_INF;
	for (int delay = 0; delay <= maxDelay; delay++) {
		double score = computeCrossCorrCoef(cum_wp, cum_w, cum_p, subvectorStart, subvectorLength, delay, xMean, yMean, global_max_delay);
		maxValue = fmax(maxValue, score);
	}
	return maxValue / denom;
}

// To avoid stack overflows :)
double cum_wp[2*MAX_WAVE_SIZE+1][MAX_WAVE_SIZE];

// Find the match score by precomputing essential metrics about pattern, wave and their correlation
double findScoreHardcore(const double* wave, int waveSize, const double* pattern, int patternSize) {
	int minSubvectorLength = 2;
	int maxDelay = patternSize - minSubvectorLength;
	int maxNegDelay = waveSize - minSubvectorLength + 1;
	// cum_wp[d][t] = sum_{i=0}^{t-1} (wave[i] * pattern[i+d])
	// for negative d the index is maxDelay-d
	cumUncorrectedCrossCorr(wave, waveSize, pattern, patternSize, cum_wp, maxDelay, maxNegDelay);
	// cumw[t] = sum_{i=0}^{t-1} (wave[i])
	double cum_w[waveSize+1];
	cumSum(wave, waveSize, cum_w);
	// y[t] = sum_{i=0}^{t-1} (pattern[i])
	double cum_p[patternSize+1];
	cumSum(pattern, patternSize, cum_p);
	// x2[t] = sum_{i=0}^{t-1} (wave[i]^2)
	double cum_w2[waveSize+1];
	cumSum2(wave, waveSize, cum_w2);
	// y2[t] = sum_{i=0}^{t-1} (pattern[i]^2)
	double cum_p2[patternSize+1];
	cumSum2(pattern, patternSize, cum_p2);

	double score = MIN_INF;
	for (int subvectorStart = 0; subvectorStart <= waveSize - minSubvectorLength; subvectorStart++) {
		for (int subvectorLength = minSubvectorLength; subvectorLength <= MIN(waveSize - subvectorStart, patternSize); subvectorLength++) {

			score = fmax(score, maxCrossCorrHardcore(cum_wp, cum_w, cum_p, cum_w2, cum_p2, subvectorStart, subvectorLength, patternSize, maxDelay) * subvectorLength);
    	}
	}
	return score;
}

int main() {
	int P, W;
	std::cin >> P >> W;
	double pattern[P];
	double wave[W];
	for (int i = 0 ; i < P; i++) {
		std::cin >> pattern[i];
	}
	for (int i = 0; i < W; i++) {
		std::cin >> wave[i];
	}
	std::cout << std::fixed << std::setprecision(4) << findScoreHardcore(wave, W, pattern, P) << std::endl;
	//std::cout << findScore(wave, W, pattern, P) << std::endl;
	return 0;
}
