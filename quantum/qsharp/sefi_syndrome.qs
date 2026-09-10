namespace SEFIQEC {

    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;

    operation MeasureSyndrome(register : Qubit[]) : Result[] {

        mutable syndrome = [];

        for q in register {
            set syndrome += [M(q)];
        }

        return syndrome;
    }
}