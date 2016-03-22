#include "MRFStereo.hpp"
#include "Constants.hpp"

/*
  mrfstereo version 1.0
  usage: ./mrfstereo [options] imL imR dispL
  options:
  -n nD          disparity levels, by default 16 (i.e. disparites 0..15)
  -b             use Birchfield/Tomasi costs
  -s             use squared differences (absolute differences by default)
  -t trunc       truncate differences to <= 'trunc'
  -a MRFalg      0-ICM, 1-Expansion (default), 2-Swap, 3-TRWS, 4-BPS, 5-BPM, 9-all
  -e smoothexp   smoothness exponent, 1 (default) or 2, i.e. L1 or L2 norm
  -m smoothmax   maximum value of smoothness term (2 by default)
  -l lambda      weight of smoothness term (20 by default)
  -g gradThresh  intensity gradient cue threshold
  -p gradPenalty if grad < gradThresh, multiply smoothness (2 by default)
  -q             quiet (turn off debugging output)
*/
void MRFStereo::compute(const int identifier) {
	std::string output = Constants::tmpDir + std::to_string(identifier) + "_output-mrf.png";
	std::string options = "-n 64 -q";
	options += " -a " + std::to_string(MRFalg);

	std::string cmd = Constants::mrfstereoBinary + " " + options;
	cmd += " " + this->imgL;
	cmd += " " + this->imgR;
	cmd += " " + output;

	system(cmd.c_str());
	cv::Mat mat = cv::imread(output, CV_LOAD_IMAGE_GRAYSCALE);
	mat.convertTo(this->result, CV_32F, 1.0 / 4);
}
